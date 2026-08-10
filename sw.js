// Service Worker for Push Notifications
self.addEventListener('push', function(event) {
    if (!event.data) return;

    try {
        const payload = event.data.json();
        
        const options = {
            body: payload.body,
            icon: payload.icon || '/static/icons/icon-192.png',
            badge: payload.badge || '/static/icons/icon-192.png',
            tag: payload.tag,
            data: payload.data,
            actions: payload.actions || [],
            requireInteraction: payload.requireInteraction !== false,
            vibrate: payload.vibrate || [200, 100, 200],
            silent: payload.silent || false,
            renotify: payload.renotify || false
        };

        event.waitUntil(
            self.registration.showNotification(payload.title, options)
        );
    } catch (e) {
        console.error('Push notification error:', e);
    }
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();

    if (event.action === 'done') {
        // Handle "Mark Done" action
        const choreId = event.notification.data?.chore_id;
        if (choreId) {
            event.waitUntil(
                fetch(`/chores/toggle/${choreId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                }).then(() => {
                    // Send message to all clients to update UI
                    self.clients.matchAll().then(clients => {
                        clients.forEach(client => {
                            client.postMessage({
                                type: 'CHORE_DONE',
                                choreId: choreId
                            });
                        });
                    });
                })
            );
        }
    } else if (event.action === 'snooze') {
        // Handle "Snooze 1hr" action - could implement later
        console.log('Snooze action clicked');
    } else {
        // Default click action - open the app
        const url = event.notification.data?.url || '/chores';
        event.waitUntil(
            clients.matchAll({ type: 'window', includeUncontrolled: true }).then(clientList => {
                for (const client of clientList) {
                    if (client.url.includes(self.location.origin) && 'focus' in client) {
                        return client.focus();
                    }
                }
                if (clients.openWindow) {
                    return clients.openWindow(url);
                }
            })
        );
    }
});

self.addEventListener('notificationclose', function(event) {
    // Optional: track notification dismissal
    console.log('Notification closed:', event.notification.tag);
});

// Handle messages from clients
self.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});

// Install event
self.addEventListener('install', function(event) {
    self.skipWaiting();
});

// Activate event
self.addEventListener('activate', function(event) {
    event.waitUntil(self.clients.claim());
});