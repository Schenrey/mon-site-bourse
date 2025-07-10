self.addEventListener('push', function(event) {
    const data = event.data.json();
    const title = 'Alerte Bourse';
    const options = {
        body: data,
        icon: '/static/icons/icon-192x192.png',
        badge: '/static/icons/badge-72x72.png'
    };
    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    event.waitUntil(
        clients.matchAll({type: 'window'}).then(clientList => {
            for (const client of clientList) {
                if (client.url === '/' && 'focus' in client) return client.focus();
            }
            if (clients.openWindow) return clients.openWindow('/');
        })
    );
});
