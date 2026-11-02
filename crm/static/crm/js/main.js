/**
 * ProCRM Main JavaScript
 * Handles responsive sidebar navigation and UI utilities.
 */

document.addEventListener('DOMContentLoaded', function () {
    // Sidebar toggle for mobile devices
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('crmSidebar');
    const backdrop = document.getElementById('crmBackdrop');

    if (sidebarToggle && sidebar && backdrop) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('show');
            backdrop.classList.toggle('show');
        });

        backdrop.addEventListener('click', function () {
            sidebar.classList.remove('show');
            backdrop.classList.remove('show');
        });
    }

    // Auto-dismiss alert notifications after 6 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            try {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
                bsAlert.close();
            } catch (e) {
                // fallback
                alert.style.display = 'none';
            }
        }, 6000);
    });
});

