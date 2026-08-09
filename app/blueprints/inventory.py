from flask import render_template, request, redirect, url_for, current_app, jsonify, flash
from ..models import db, InventoryItem
from ..blueprints import main_bp
from ..security import sanitize_text
import json


def _admin_aliases() -> set[str]:
    admin_name = current_app.config['HOMEHUB_CONFIG'].get('admin_name', 'Administrator')
    return {admin_name, 'Administrator', 'admin'}


def _request_user() -> str:
    return sanitize_text(request.form.get('user', ''))


def _render_inventory_page(**form_state):
    filter_category = request.args.get('category')
    filter_location = request.args.get('location')
    filter_low_stock = request.args.get('low_stock') in ('1', 'on', 'true', 'yes')
    
    query = InventoryItem.query.order_by(InventoryItem.category.asc(), InventoryItem.name.asc())
    
    if filter_category:
        query = query.filter(InventoryItem.category == filter_category)
    if filter_location:
        query = query.filter(InventoryItem.location == filter_location)
    
    items = query.all()
    
    if filter_low_stock:
        items = [i for i in items if i.quantity <= i.min_quantity]
    
    # Get unique categories and locations for filters
    all_items = InventoryItem.query.all()
    categories = sorted(set(i.category for i in all_items if i.category))
    locations = sorted(set(i.location for i in all_items if i.location))
    
    config = current_app.config['HOMEHUB_CONFIG']
    return render_template(
        'inventory.html',
        items=items,
        categories=categories,
        locations=locations,
        filter_category=filter_category,
        filter_location=filter_location,
        filter_low_stock=filter_low_stock,
        **form_state,
        config=config,
    )


@main_bp.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        name = sanitize_text(request.form['name'])
        creator = sanitize_text(request.form['creator'])
        user = _request_user()
        admin_aliases = _admin_aliases()
        
        try:
            quantity = float(request.form.get('quantity') or 0)
        except ValueError:
            quantity = 0.0
            
        unit = sanitize_text(request.form.get('unit', 'pcs'))
        category = sanitize_text(request.form.get('category', ''))
        location = sanitize_text(request.form.get('location', ''))
        
        try:
            min_quantity = float(request.form.get('min_quantity') or 0)
        except ValueError:
            min_quantity = 0.0
            
        raw_tags = request.form.get('tags', '').strip()
        tags_list = []
        if raw_tags:
            try:
                tags_list = json.loads(raw_tags)
                if not isinstance(tags_list, list):
                    tags_list = []
            except Exception:
                tags_list = [t.strip() for t in raw_tags.split(',') if t.strip()]
        tags_list = [sanitize_text(t) for t in tags_list if isinstance(t, str) and t.strip()]
        
        if item_id:
            item = InventoryItem.query.get_or_404(int(item_id))
            if not (user in admin_aliases or user == (item.creator or '')):
                flash('Not allowed to update item.', 'error')
                return redirect(url_for('main.inventory'))
            item.name = name
            item.quantity = quantity
            item.unit = unit
            item.category = category
            item.location = location
            item.min_quantity = min_quantity
            item.tags = json.dumps(tags_list)
            db.session.commit()
            flash('Item updated.', 'success')
        else:
            item = InventoryItem(
                name=name,
                quantity=quantity,
                unit=unit,
                category=category,
                location=location,
                min_quantity=min_quantity,
                creator=creator,
                tags=json.dumps(tags_list),
            )
            db.session.add(item)
            db.session.commit()
            flash('Item added.', 'success')
        return redirect(url_for('main.inventory'))
    return _render_inventory_page()


@main_bp.route('/inventory/edit/<int:item_id>')
def edit_inventory_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    user = request.args.get('user')
    if not user:
        user = request.args.get('creator')
    user = sanitize_text(user or '')
    admin_aliases = _admin_aliases()
    creator = (item.creator or '')
    if not (user in admin_aliases or user == creator):
        flash('Not allowed to edit item.', 'error')
        return redirect(url_for('main.inventory'))
    try:
        item_tags = json.loads(item.tags or '[]')
    except Exception:
        item_tags = []
    form_state = {
        'form_name': item.name,
        'form_quantity': item.quantity,
        'form_unit': item.unit,
        'form_category': item.category,
        'form_location': item.location,
        'form_min_quantity': item.min_quantity,
        'form_tags': json.dumps(item_tags),
        'form_item_id': item.id,
    }
    return _render_inventory_page(**form_state)


@main_bp.route('/inventory/delete/<int:item_id>', methods=['POST'])
def delete_inventory_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    user = sanitize_text(request.form.get('user', ''))
    admin_aliases = _admin_aliases()
    if user in admin_aliases or user == item.creator:
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted.', 'success')
    else:
        flash('Not allowed to delete item.', 'error')
    return redirect(url_for('main.inventory'))


@main_bp.route('/inventory/adjust/<int:item_id>', methods=['POST'])
def adjust_inventory_quantity(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    try:
        data = request.get_json(force=True) or {}
        user = sanitize_text(str(data.get('user', '')))
        admin_aliases = _admin_aliases()
        if not (user in admin_aliases or user == (item.creator or '')):
            return jsonify({"ok": False, "error": "not allowed"}), 403
        delta = data.get('delta')
        if delta is None:
            return jsonify({"ok": False, "error": "delta required"}), 400
        try:
            delta = float(delta)
        except (ValueError, TypeError):
            return jsonify({"ok": False, "error": "invalid delta"}), 400
        item.quantity = max(0, item.quantity + delta)
        db.session.commit()
        return jsonify({"ok": True, "id": item.id, "quantity": item.quantity})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


@main_bp.route('/api/inventory', methods=['GET'])
def api_get_inventory():
    filter_category = request.args.get('category')
    filter_location = request.args.get('location')
    filter_low_stock = request.args.get('low_stock') in ('1', 'on', 'true', 'yes')
    
    query = InventoryItem.query.order_by(InventoryItem.category.asc(), InventoryItem.name.asc())
    
    if filter_category:
        query = query.filter(InventoryItem.category == filter_category)
    if filter_location:
        query = query.filter(InventoryItem.location == filter_location)
    
    items = query.all()
    
    if filter_low_stock:
        items = [i for i in items if i.quantity <= i.min_quantity]
    
    def to_dict(i):
        try:
            tg = json.loads(i.tags or '[]')
        except Exception:
            tg = []
        return {
            "id": i.id,
            "name": i.name,
            "quantity": i.quantity,
            "unit": i.unit,
            "category": i.category,
            "location": i.location,
            "min_quantity": i.min_quantity,
            "creator": i.creator,
            "timestamp": i.timestamp.isoformat() if i.timestamp else None,
            "updated_at": i.updated_at.isoformat() if i.updated_at else None,
            "tags": tg,
            "is_low_stock": i.quantity <= i.min_quantity,
        }
    return jsonify([to_dict(i) for i in items])