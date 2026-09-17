/**
 * StudentHub — JavaScript Interactivity Helper
 */

document.addEventListener('DOMContentLoaded', () => {
  // Sidebar Toggle
  const sidebarCollapse = document.getElementById('sidebarCollapse');
  const sidebar = document.getElementById('sidebar');

  if (sidebarCollapse && sidebar) {
    sidebarCollapse.addEventListener('click', () => {
      sidebar.classList.toggle('active');
    });
  }

  // Auto Dismiss Alerts after 5 seconds
  const autoAlerts = document.querySelectorAll('.alert-dismissible');
  autoAlerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });
});
