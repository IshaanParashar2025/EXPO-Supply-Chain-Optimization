// App Initialization & Navigation
function showPage(pageId, navEl) {
  // Hide all pages
  document.querySelectorAll('.page').forEach(page => {
    page.classList.remove('active');
  });

  // Show selected page
  const page = document.getElementById(pageId);
  if (page) page.classList.add('active');

  // Update nav active
  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.remove('active');
  });
  if (navEl) navEl.classList.add('active');

  // Load data for page
  const actions = {
    'dashboard': refreshDashboard,
    'suppliers': refreshSuppliers,
    'manufacturers': refreshManufacturers,
    'distributors': refreshDistributors,
    'inventory': refreshInventory,
    'orders': refreshOrders,
    'logistics': refreshLogistics,
  };
  if (actions[pageId]) actions[pageId]();
}
window.showPage = showPage;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
  console.log("EXPO's Supply Chain MVC App Loaded");
  hideLoader();
  refreshDashboard();
  populateSelects();
});

