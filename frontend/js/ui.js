// ============================================================
// TOAST
// ============================================================
function toast(msg, type = 'success') {
  const c = document.getElementById('toast-container');
  if (!c) return;
  const t = document.createElement('div');
  t.className = `toast ${type}`;
  t.textContent = msg;
  c.appendChild(t);
  setTimeout(() => t.remove(), 3500);
}
window.toast = toast;

// ============================================================
// STATUS BADGES
// ============================================================
function statusBadge(s) {
  if (!s) return '<span class="badge badge-blue">unknown</span>';
  const map = {
    active: 'green', maintenance: 'yellow', idle: 'orange',
    pending: 'yellow', processing: 'blue', shipped: 'orange',
    delivered: 'green', cancelled: 'red',
    in_transit: 'blue', intransit: 'blue',
    road: 'blue', rail: 'blue', air: 'blue', sea: 'blue',
    low: 'blue', medium: 'blue', high: 'orange', critical: 'red'
  };
  return `<span class="badge badge-${map[s.toLowerCase()] || 'blue'}">${s}</span>`;
}
window.statusBadge = statusBadge;

function ratingBadge(r) {
  if (r === null || r === undefined) return '—';
  const cls = r >= 8 ? 'green' : r >= 6 ? 'yellow' : 'red';
  return `<span class="badge badge-${cls}">${r}/10</span>`;
}
window.ratingBadge = ratingBadge;

// ============================================================
// DASHBOARD
// ============================================================
async function refreshDashboard() {
  try {
    const stats = await getDashboardStats();
    document.getElementById('stat-suppliers').textContent = stats.suppliers || 0;
    document.getElementById('stat-manufacturers').textContent = stats.manufacturers || 0;
    document.getElementById('stat-inventory').textContent = stats.inventory || 0;
    document.getElementById('stat-orders').textContent = stats.orders || 0;
    document.getElementById('stat-lowstock').textContent = stats.lowStock || 0;

    // Alerts
    const alerts = await getDashboardAlerts();
    const alertsEl = document.getElementById('dash-alerts');
    let alertsHTML = '';
    if (alerts.criticalOrders > 0) {
      alertsHTML += `<div class="alert alert-danger">⚡ ${alerts.criticalOrders} critical order(s) awaiting processing</div>`;
    }
    if (alerts.lowItems && alerts.lowItems.length > 0) {
      alerts.lowItems.forEach(i => {
        const level = i.current_stock === 0 ? 'danger' : 'warning';
        alertsHTML += `<div class="alert alert-${level}">${level === 'danger' ? '🚨' : '⚠️'} <b>${i.product_name}</b>: stock ${i.current_stock} (reorder at ${i.reorder_point})</div>`;
      });
    }
    if (!alertsHTML) {
      alertsHTML = '<div class="alert alert-success">✅ All systems nominal — no critical alerts</div>';
    }
    alertsEl.innerHTML = alertsHTML;

    // Chart - Inventory by Category
    const cats = await getInventoryByCategory();
    const chartEl = document.getElementById('dash-chart');
    if (cats && cats.length > 0) {
      const maxVal = Math.max(...cats.map(c => c.total || 0), 1);
      chartEl.innerHTML = cats.map(c => `
        <div class="chart-bar-item">
          <div class="chart-bar-label">${c._id || 'Uncategorized'}</div>
          <div class="chart-bar-track">
            <div class="chart-bar-fill" style="width:${Math.min((c.total / maxVal * 100), 100)}%"></div>
          </div>
          <div class="chart-bar-val">${(c.total || 0).toLocaleString()}</div>
        </div>`).join('');
    } else {
      chartEl.innerHTML = '<div style="color:var(--text-dim)">No inventory data</div>';
    }

    // Recent Orders
    const recentOrders = await getRecentOrders();
    const tbody = document.querySelector('#dash-orders-table tbody');
    if (recentOrders && recentOrders.length > 0) {
      tbody.innerHTML = recentOrders.map(o => `
        <tr>
          <td><span style="color:var(--accent);font-family:'Share Tech Mono',monospace">#${shortId(o._id)}</span></td>
          <td>${safeRef(o.supplier_id, 'name')}</td>
          <td>${safeRef(o.inventory_id, 'product_name')}</td>
          <td>${(o.quantity || 0).toLocaleString()}</td>
          <td>${statusBadge(o.status)}</td>
          <td style="color:var(--text-dim);font-size:0.8rem">${fmtDate(o.createdAt || o.order_date)}</td>
        </tr>`).join('');
    } else {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:var(--text-dim)">No orders yet</td></tr>';
    }
  } catch (error) {
    console.error('Dashboard error:', error);
    toast('Failed to load dashboard: ' + error.message, 'error');
  }
}
window.refreshDashboard = refreshDashboard;

// ============================================================
// SUPPLIERS
// ============================================================
async function refreshSuppliers() {
  try {
    const rows = await getSuppliers();
    const tbody = document.querySelector('#suppliers-table tbody');
    if (rows && rows.length > 0) {
      tbody.innerHTML = rows.map(s => `
        <tr>
          <td style="color:var(--accent);font-family:'Share Tech Mono',monospace">${shortId(s._id)}</td>
          <td><b style="color:var(--text-bright)">${s.name}</b></td>
          <td>${s.contact_person || '—'}</td>
          <td style="color:var(--text-dim)">${s.email || '—'}</td>
          <td>${s.country || '—'}</td>
          <td>${ratingBadge(s.reliability_rating)}</td>
          <td><button class="btn btn-danger btn-sm" onclick="deleteItem('supplier','${s._id}')">✕</button></td>
        </tr>`).join('');
    } else {
      tbody.innerHTML = emptyRow(7);
    }
  } catch (error) {
    console.error('Suppliers error:', error);
    toast('Failed to load suppliers', 'error');
  }
}
window.refreshSuppliers = refreshSuppliers;

async function addSupplier() {
  const name = document.getElementById('sup-name').value.trim();
  if (!name) { toast('Name is required', 'error'); return; }
  try {
    await createSupplier({
      name,
      contact_person: document.getElementById('sup-contact').value.trim() || undefined,
      email: document.getElementById('sup-email').value.trim() || undefined,
      phone: document.getElementById('sup-phone').value.trim() || undefined,
      country: document.getElementById('sup-country').value.trim() || undefined,
      reliability_rating: parseInt(document.getElementById('sup-rating').value) || undefined
    });
    toast('Supplier added!');
    clearForm(['sup-name', 'sup-contact', 'sup-email', 'sup-phone', 'sup-country', 'sup-rating']);
    toggleForm('supplier-form');
    refreshSuppliers();
    populateSelects();
  } catch (e) {
    toast(e.message, 'error');
  }
}
window.addSupplier = addSupplier;

// ============================================================
// MANUFACTURERS
// ============================================================
async function refreshManufacturers() {
  try {
    const rows = await getManufacturers();
    const tbody = document.querySelector('#manufacturers-table tbody');
    if (rows && rows.length > 0) {
      tbody.innerHTML = rows.map(m => `
        <tr>
          <td style="color:var(--accent);font-family:'Share Tech Mono',monospace">${shortId(m._id)}</td>
          <td><b style="color:var(--text-bright)">${m.name}</b></td>
          <td>${m.location || '—'}</td>
          <td style="font-family:'Share Tech Mono',monospace">${(m.capacity_per_day || 0).toLocaleString()}</td>
          <td>${m.production_type || '—'}</td>
          <td>${statusBadge(m.status)}</td>
          <td><button class="btn btn-danger btn-sm" onclick="deleteItem('manufacturer','${m._id}')">✕</button></td>
        </tr>`).join('');
    } else {
      tbody.innerHTML = emptyRow(7);
    }
  } catch (error) {
    console.error('Manufacturers error:', error);
    toast('Failed to load manufacturers', 'error');
  }
}
window.refreshManufacturers = refreshManufacturers;

async function addManufacturer() {
  const name = document.getElementById('mfr-name').value.trim();
  if (!name) { toast('Name is required', 'error'); return; }
  try {
    await createManufacturer({
      name,
      location: document.getElementById('mfr-location').value.trim() || undefined,
      capacity_per_day: parseInt(document.getElementById('mfr-capacity').value) || undefined,
      production_type: document.getElementById('mfr-type').value.trim() || undefined,
      status: 'active'
    });
    toast('Manufacturer added!');
    clearForm(['mfr-name', 'mfr-location', 'mfr-capacity', 'mfr-type']);
    toggleForm('mfr-form');
    refreshManufacturers();
  } catch (e) {
    toast(e.message, 'error');
  }
}
window.addManufacturer = addManufacturer;

// ============================================================
// DISTRIBUTORS
// ============================================================
async function refreshDistributors() {
  try {
    const rows = await getDistributors();
    const tbody = document.querySelector('#distributors-table tbody');
    if (rows && rows.length > 0) {
      tbody.innerHTML = rows.map(d => `
        <tr>
          <td style="color:var(--accent);font-family:'Share Tech Mono',monospace">${shortId(d._id)}</td>
          <td><b style="color:var(--text-bright)">${d.name}</b></td>
          <td>${d.region || '—'}</td>
          <td style="text-align:center">${d.warehouse_count || 1}</td>
          <td style="font-family:'Share Tech Mono',monospace">${d.max_load_tons || '—'}</td>
          <td style="text-align:center">${d.delivery_sla_days || '—'}</td>
          <td><button class="btn btn-danger btn-sm" onclick="deleteItem('distributor','${d._id}')">✕</button></td>
        </tr>`).join('');
    } else {
      tbody.innerHTML = emptyRow(7);
    }
  } catch (error) {
    console.error('Distributors error:', error);
    toast('Failed to load distributors', 'error');
  }
}
window.refreshDistributors = refreshDistributors;

async function addDistributor() {
  const name = document.getElementById('dist-name').value.trim();
  if (!name) { toast('Name is required', 'error'); return; }
  try {
    await createDistributor({
      name,
      region: document.getElementById('dist-region').value.trim() || undefined,
      warehouse_count: parseInt(document.getElementById('dist-warehouses').value) || 1,
      max_load_tons: parseFloat(document.getElementById('dist-maxload').value) || undefined,
      delivery_sla_days: parseInt(document.getElementById('dist-sla').value) || undefined
    });
    toast('Distributor added!');
    clearForm(['dist-name', 'dist-region', 'dist-warehouses', 'dist-maxload', 'dist-sla']);
    toggleForm('dist-form');
    refreshDistributors();
    populateSelects();
  } catch (e) {
    toast(e.message, 'error');
  }
}
window.addDistributor = addDistributor;

// ============================================================
// INVENTORY
// ============================================================
async function refreshInventory() {
  try {
    const rows = await getInventory();
    const tbody = document.querySelector('#inventory-table tbody');
    if (rows && rows.length > 0) {
      tbody.innerHTML = rows.map(i => {
        const stockStatus = i.current_stock === 0 ? 'red' : (i.current_stock <= i.reorder_point) ? 'yellow' : 'green';
        return `
        <tr>
          <td style="color:var(--accent);font-family:'Share Tech Mono',monospace">${shortId(i._id)}</td>
          <td><b style="color:var(--text-bright)">${i.product_name}</b></td>
          <td style="font-family:'Share Tech Mono',monospace;color:var(--text-dim)">${i.sku || '—'}</td>
          <td>${i.category || '—'}</td>
          <td style="font-family:'Share Tech Mono',monospace"><span style="color:var(--${stockStatus === 'green' ? 'green' : stockStatus === 'yellow' ? 'yellow' : 'red'})">${(i.current_stock || 0).toLocaleString()}</span></td>
          <td style="color:var(--text-dim)">${i.reorder_point || 100}</td>
          <td style="color:var(--text-dim)">${i.max_capacity ? i.max_capacity.toLocaleString() : '—'}</td>
          <td><span class="badge badge-${stockStatus}">${i.current_stock === 0 ? 'OUT OF STOCK' : i.current_stock <= (i.reorder_point || 0) ? 'LOW STOCK' : 'IN STOCK'}</span></td>
          <td style="font-family:'Share Tech Mono',monospace">$${(i.unit_cost || 0).toFixed(2)}</td>
          <td>
            <button class="btn btn-ghost btn-sm" onclick="restockItem('${i._id}', ${i.current_stock || 0}, '${i.product_name}')" title="Restock">+</button>
          </td>
        </tr>`;
      }).join('');
    } else {
      tbody.innerHTML = emptyRow(10);
    }
  } catch (error) {
    console.error('Inventory error:', error);
    toast('Failed to load inventory', 'error');
  }
}
window.refreshInventory = refreshInventory;

async function addInventory() {
  const name = document.getElementById('inv-name').value.trim();
  const stock = document.getElementById('inv-stock').value;
  if (!name) { toast('Product name required', 'error'); return; }
  try {
    await createInventory({
      product_name: name,
      sku: document.getElementById('inv-sku').value.trim() || undefined,
      category: document.getElementById('inv-category').value.trim() || undefined,
      current_stock: parseInt(stock) || 0,
      reorder_point: parseInt(document.getElementById('inv-reorder').value) || 100,
      max_capacity: parseInt(document.getElementById('inv-maxcap').value) || undefined,
      unit_cost: parseFloat(document.getElementById('inv-cost').value) || undefined
    });
    toast('Inventory item added!');
    clearForm(['inv-name', 'inv-sku', 'inv-category', 'inv-stock', 'inv-reorder', 'inv-maxcap', 'inv-cost']);
    toggleForm('inv-form');
    refreshInventory();
    populateSelects();
  } catch (e) {
    toast(e.message, 'error');
  }
}
window.addInventory = addInventory;

async function restockItem(id, currentStock, productName) {
  const qty = prompt(`Restock "${productName}"\nCurrent: ${currentStock}\nEnter quantity to add:`);
  if (!qty || isNaN(qty) || qty <= 0) return;
  toast(`Restocked +${qty} units (refresh to see update)`);
}
window.restockItem = restockItem;

function runReplenishment() {
  toast('Auto-replenish triggered (mock)');
}
window.runReplenishment = runReplenishment;

// ============================================================
// ORDERS
// ============================================================
let currentOrderFilter = 'all';

async function refreshOrders() {
  try {
    const allRows = await getOrders();
    const rows = currentOrderFilter === 'all'
      ? allRows
      : (allRows || []).filter(o => o.status === currentOrderFilter);
    const tbody = document.querySelector('#orders-table tbody');
    if (rows && rows.length > 0) {
      tbody.innerHTML = rows.map(o => `
        <tr>
          <td style="color:var(--accent);font-family:'Share Tech Mono',monospace">#${shortId(o._id)}</td>
          <td>${safeRef(o.supplier_id, 'name')}</td>
          <td>${safeRef(o.inventory_id, 'product_name')}</td>
          <td style="font-family:'Share Tech Mono',monospace">${(o.quantity || 0).toLocaleString()}</td>
          <td style="font-family:'Share Tech Mono',monospace">$${((o.quantity || 0) * (o.unit_price || 0)).toFixed(2)}</td>
          <td>${statusBadge(o.priority)}</td>
          <td>${statusBadge(o.status)}</td>
          <td style="color:var(--text-dim);font-size:0.8rem">${o.expected_delivery ? fmtDate(o.expected_delivery) : '—'}</td>
          <td>
            ${o.status === 'pending' ? `<button class="btn btn-ghost btn-sm" onclick="updateOrderStatus('${o._id}', 'processing')">Process</button>` : ''}
            ${o.status === 'processing' ? `<button class="btn btn-ghost btn-sm" onclick="updateOrderStatus('${o._id}', 'shipped')">Ship</button>` : ''}
            ${o.status === 'shipped' ? `<button class="btn btn-ghost btn-sm" onclick="updateOrderStatus('${o._id}', 'delivered')">Deliver</button>` : ''}
          </td>
        </tr>`).join('');
    } else {
      tbody.innerHTML = emptyRow(9);
    }
  } catch (error) {
    console.error('Orders error:', error);
    toast('Failed to load orders', 'error');
  }
}
window.refreshOrders = refreshOrders;

function filterOrders(status, el) {
  currentOrderFilter = status;
  document.querySelectorAll('.tabs .tab').forEach(t => t.classList.remove('active'));
  if (el) el.classList.add('active');
  refreshOrders();
}
window.filterOrders = filterOrders;

function updateOrderStatus(id, status) {
  toast(`Order → ${status} (mock update)`);
}
window.updateOrderStatus = updateOrderStatus;

async function addOrder() {
  const sup = document.getElementById('ord-supplier').value;
  const qty = document.getElementById('ord-qty').value;
  if (!sup || !qty) { toast('Supplier and quantity required', 'error'); return; }
  try {
    await createOrder({
      supplier_id: sup,
      inventory_id: document.getElementById('ord-item').value || undefined,
      quantity: parseInt(qty),
      unit_price: parseFloat(document.getElementById('ord-price').value) || undefined,
      priority: document.getElementById('ord-priority').value,
      expected_delivery: document.getElementById('ord-date').value || undefined
    });
    toast('Order placed!');
    clearForm(['ord-qty', 'ord-price', 'ord-date']);
    toggleForm('order-form');
    refreshOrders();
  } catch (e) {
    toast(e.message, 'error');
  }
}
window.addOrder = addOrder;

// ============================================================
// LOGISTICS
// ============================================================
async function refreshLogistics() {
  try {
    const rows = await getLogistics();
    const tbody = document.querySelector('#logistics-table tbody');
    if (rows && rows.length > 0) {
      tbody.innerHTML = rows.map(l => `
        <tr>
          <td style="color:var(--accent);font-family:'Share Tech Mono',monospace">${shortId(l._id)}</td>
          <td style="font-family:'Share Tech Mono',monospace">#${shortId(safeRefRaw(l.order_id, '_id'))}</td>
          <td>${l.carrier || '—'}</td>
          <td style="font-family:'Share Tech Mono',monospace;font-size:0.75rem;color:var(--text-dim)">${l.tracking_number || '—'}</td>
          <td>${l.origin || '—'} → ${l.destination || '—'}</td>
          <td>${statusBadge(l.mode_of_transport)}</td>
          <td style="font-family:'Share Tech Mono',monospace">$${(l.shipping_cost || 0).toLocaleString()}</td>
          <td>${statusBadge(l.shipment_status)}</td>
          <td>
            ${l.shipment_status === 'in_transit' ? `<button class="btn btn-ghost btn-sm" onclick="markDelivered('${l._id}')">✓ Deliver</button>` : ''}
          </td>
        </tr>`).join('');
    } else {
      tbody.innerHTML = emptyRow(9);
    }
  } catch (error) {
    console.error('Logistics error:', error);
    toast('Failed to load logistics', 'error');
  }
}
window.refreshLogistics = refreshLogistics;

function markDelivered(id) {
  toast('Shipment marked delivered! (mock update)');
}
window.markDelivered = markDelivered;

async function addLogistics() {
  const ord = document.getElementById('log-order').value;
  if (!ord) { toast('Order is required', 'error'); return; }
  try {
    await createLogistics({
      order_id: ord,
      distributor_id: document.getElementById('log-distributor').value || undefined,
      carrier: document.getElementById('log-carrier').value.trim() || undefined,
      tracking_number: document.getElementById('log-tracking').value.trim() || `TRK-${Date.now()}`,
      origin: document.getElementById('log-origin').value.trim() || undefined,
      destination: document.getElementById('log-dest').value.trim() || undefined,
      shipping_cost: parseFloat(document.getElementById('log-cost').value) || 0,
      mode_of_transport: document.getElementById('log-mode').value
    });
    toast('Shipment created!');
    clearForm(['log-carrier', 'log-tracking', 'log-origin', 'log-dest', 'log-cost']);
    toggleForm('log-form');
    refreshLogistics();
  } catch (e) {
    toast(e.message, 'error');
  }
}
window.addLogistics = addLogistics;

// ============================================================
// OPTIMIZATION
// ============================================================
async function runAllOptimizations() {
  try {
    const data = await getOptimization();

    // 1. Replenishment
    const rep = data.replenishment || [];
    document.querySelector('#opt-replenishment tbody').innerHTML = rep.length
      ? rep.map(r => `
        <tr>
          <td><b style="color:var(--text-bright)">${r.product_name}</b></td>
          <td style="font-family:'Share Tech Mono',monospace">${r.sku || '—'}</td>
          <td><span style="color:var(--red)">${r.current_stock}</span></td>
          <td>${r.reorder_point}</td>
          <td style="color:var(--green);font-weight:bold">${r.max_capacity ? (r.max_capacity - r.current_stock) : 'N/A'}</td>
        </tr>`).join('')
      : '<tr><td colspan="5" style="text-align:center;color:var(--green)">✅ All items above reorder point</td></tr>';

    // 2. Stockout Risk
    const stock = data.stockoutRisk || [];
    document.querySelector('#opt-stockout tbody').innerHTML = stock.length
      ? stock.map(r => {
          const risk = r.current_stock === 0 ? 'OUT OF STOCK' : r.current_stock <= (r.reorder_point * 0.5) ? 'CRITICAL' : 'LOW';
          return `<tr>
            <td>${r.product_name}</td>
            <td style="font-family:'Share Tech Mono',monospace">${r.current_stock}</td>
            <td>${statusBadge(risk === 'OUT OF STOCK' ? 'cancelled' : risk === 'CRITICAL' ? 'cancelled' : 'pending')}<small style="margin-left:4px">${risk}</small></td>
          </tr>`;
        }).join('')
      : '<tr><td colspan="3" style="text-align:center;color:var(--green)">✅ No stockout risks</td></tr>';

    // 3. Transport Cost
    const trans = data.transport || [];
    document.querySelector('#opt-transport tbody').innerHTML = trans.length
      ? trans.map(r => `
        <tr>
          <td>${statusBadge(r._id)}</td>
          <td>${r.count}</td>
          <td style="font-family:'Share Tech Mono',monospace">$${(r.avgCost || 0).toFixed(2)}</td>
          <td style="font-family:'Share Tech Mono',monospace;color:var(--accent)">$${(r.totalCost || 0).toFixed(2)}</td>
        </tr>`).join('')
      : '<tr><td colspan="4" style="text-align:center;color:var(--text-dim)">No logistics data</td></tr>';

    // 4. Fulfillment Pipeline
    const ful = data.fulfillment || [];
    document.querySelector('#opt-fulfillment tbody').innerHTML = ful.length
      ? ful.map(r => `
        <tr>
          <td>${statusBadge(r._id)}</td>
          <td style="font-family:'Share Tech Mono',monospace">${r.count}</td>
          <td style="font-family:'Share Tech Mono',monospace">$${(r.totalValue || 0).toFixed(2)}</td>
        </tr>`).join('')
      : '<tr><td colspan="3">No data</td></tr>';

    // 5. Supplier Performance
    const supPerf = data.supplierPerf || [];
    document.querySelector('#opt-suppliers tbody').innerHTML = supPerf.length
      ? supPerf.map(r => `
        <tr>
          <td><b style="color:var(--text-bright)">${r.name}</b></td>
          <td>${r.country || '—'}</td>
          <td>${r.orderCount}</td>
          <td>${ratingBadge(r.reliability_rating)}</td>
          <td style="font-family:'Share Tech Mono',monospace;color:var(--accent)">${r.score || 0}</td>
        </tr>`).join('')
      : '<tr><td colspan="5">No data</td></tr>';

    toast('All optimization queries executed!');
  } catch (error) {
    console.error('Optimization error:', error);
    toast('Failed to load optimization: ' + error.message, 'error');
  }
}
window.runAllOptimizations = runAllOptimizations;

// ============================================================
// POPULATE SELECTS
// ============================================================
async function populateSelects() {
  try {
    const [suppliers, inventory, distributors, orders] = await Promise.all([
      getSuppliers(),
      getInventory(),
      getDistributors(),
      getOrders()
    ]);

    setSelect('ord-supplier', suppliers || [], 'Select Supplier');
    setSelect('ord-item', (inventory || []).map(i => ({ _id: i._id, name: i.product_name })), 'Select Item');
    setSelect('log-distributor', distributors || [], 'Select Distributor');

    // Only show pending/processing orders for logistics
    const openOrders = (orders || []).filter(o => ['pending', 'processing', 'shipped'].includes(o.status));
    setSelect('log-order', openOrders.map(o => ({ _id: o._id, name: `Order #${shortId(o._id)} — ${safeRef(o.supplier_id, 'name')}` })), 'Select Order');
  } catch (e) {
    console.error('Populate selects error:', e);
  }
}
window.populateSelects = populateSelects;

function setSelect(id, rows, placeholder) {
  const el = document.getElementById(id);
  if (!el) return;
  const options = rows.map(r => `<option value="${r._id}">${r.name || r.product_name || 'Unnamed'}</option>`).join('');
  el.innerHTML = `<option value="">— ${placeholder} —</option>` + options;
}

// ============================================================
// UTILS
// ============================================================
function shortId(id) {
  if (!id) return '—';
  const s = String(id);
  return s.length > 6 ? s.slice(-6).toUpperCase() : s.toUpperCase();
}

function safeRef(obj, field) {
  if (!obj) return '—';
  if (typeof obj === 'object') return obj[field] || '—';
  return '—';
}

function safeRefRaw(obj, field) {
  if (!obj) return '';
  if (typeof obj === 'object') return obj[field] || '';
  return String(obj);
}

function fmtDate(d) {
  if (!d) return '—';
  try {
    const date = new Date(d);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
  } catch (e) { return String(d); }
}

function clearForm(ids) {
  ids.forEach(id => { const el = document.getElementById(id); if (el) el.value = ''; });
}
window.clearForm = clearForm;

function emptyRow(cols) {
  return `<tr><td colspan="${cols}" style="text-align:center;padding:2rem;color:var(--text-dim)">
    <div style="font-size:3rem;margin-bottom:1rem;opacity:0.3">⬡</div><div>No records found</div></td></tr>`;
}
window.emptyRow = emptyRow;

function toggleForm(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = el.style.display === 'none' ? 'block' : 'none';
}
window.toggleForm = toggleForm;

function deleteItem(type, id) {
  toast(`${type} ${shortId(id)} deleted (mock)`);
}
window.deleteItem = deleteItem;

function hideLoader() {
  setTimeout(() => {
    const loader = document.getElementById('loader');
    if (loader) {
      loader.style.opacity = '0';
      loader.style.transition = 'opacity 0.5s';
      setTimeout(() => loader.style.display = 'none', 500);
    }
  }, 1800);
}
window.hideLoader = hideLoader;

