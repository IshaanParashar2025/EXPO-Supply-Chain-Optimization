const BASE_URL = window.API_BASE_URL || 'http://localhost:5000/api';

// Dashboard
async function getDashboardStats() {
  const response = await fetch(`${BASE_URL}/dashboard/stats`);
  if (!response.ok) throw new Error('Failed to fetch stats');
  return await response.json();
}

async function getDashboardAlerts() {
  const response = await fetch(`${BASE_URL}/dashboard/alerts`);
  if (!response.ok) throw new Error('Failed to fetch alerts');
  return await response.json();
}

async function getInventoryByCategory() {
  const response = await fetch(`${BASE_URL}/dashboard/inventory-by-category`);
  if (!response.ok) throw new Error('Failed to fetch category data');
  return await response.json();
}

async function getRecentOrders() {
  const response = await fetch(`${BASE_URL}/dashboard/recent-orders`);
  if (!response.ok) throw new Error('Failed to fetch recent orders');
  return await response.json();
}

async function getOptimization() {
  const response = await fetch(`${BASE_URL}/dashboard/optimization`);
  if (!response.ok) throw new Error('Failed to fetch optimization data');
  return await response.json();
}

// Core CRUD
async function getSuppliers() {
  const response = await fetch(`${BASE_URL}/suppliers`);
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  return await response.json();
}

async function createSupplier(data) {
  const response = await fetch(`${BASE_URL}/suppliers`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error(`Failed: ${response.statusText}`);
  return await response.json();
}

async function getManufacturers() {
  const response = await fetch(`${BASE_URL}/manufacturers`);
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  return await response.json();
}

async function createManufacturer(data) {
  const response = await fetch(`${BASE_URL}/manufacturers`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error(`Failed: ${response.statusText}`);
  return await response.json();
}

async function getDistributors() {
  const response = await fetch(`${BASE_URL}/distributors`);
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  return await response.json();
}

async function createDistributor(data) {
  const response = await fetch(`${BASE_URL}/distributors`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error(`Failed: ${response.statusText}`);
  return await response.json();
}

async function getInventory() {
  const response = await fetch(`${BASE_URL}/inventory`);
  return await response.json();
}

async function createInventory(data) {
  const response = await fetch(`${BASE_URL}/inventory`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error(`Failed: ${response.statusText}`);
  return await response.json();
}

async function getOrders() {
  const response = await fetch(`${BASE_URL}/orders`);
  return await response.json();
}

async function createOrder(data) {
  const response = await fetch(`${BASE_URL}/orders`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error(`Failed: ${response.statusText}`);
  return await response.json();
}

async function getLogistics() {
  const response = await fetch(`${BASE_URL}/logistics`);
  return await response.json();
}

async function createLogistics(data) {
  const response = await fetch(`${BASE_URL}/logistics`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error(`Failed: ${response.statusText}`);
  return await response.json();
}

// Globals
window.getDashboardStats = getDashboardStats;
window.getDashboardAlerts = getDashboardAlerts;
window.getInventoryByCategory = getInventoryByCategory;
window.getRecentOrders = getRecentOrders;
window.getOptimization = getOptimization;
window.getSuppliers = getSuppliers;
window.createSupplier = createSupplier;
window.getManufacturers = getManufacturers;
window.createManufacturer = createManufacturer;
window.getDistributors = getDistributors;
window.createDistributor = createDistributor;
window.getInventory = getInventory;
window.createInventory = createInventory;
window.getOrders = getOrders;
window.createOrder = createOrder;
window.getLogistics = getLogistics;
window.createLogistics = createLogistics;

