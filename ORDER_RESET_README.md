# Order ID Reset Documentation

## Problem
When orders are deleted from the Django admin backend, the auto-increment sequence for order IDs continues from the last used ID instead of starting from 1.

## Solution
Created Django management commands to reset the order ID sequence to start from 1.

## Usage

### Method 1: After manually deleting orders from admin (RECOMMENDED)
```bash
python manage.py force_reset_orders
```

### Method 2: Delete all orders and reset sequence
```bash
python manage.py reset_all_orders --confirm
```

### Method 3: Reset sequence only (if no orders exist)
```bash
python manage.py reset_order_sequence
```

## Step-by-Step Instructions

1. **Delete orders from Django admin:**
   - Go to http://127.0.0.1:8000/admin/
   - Navigate to Payment → Orders
   - Select all orders and delete them

2. **Reset the sequence:**
   ```bash
   python manage.py force_reset_orders
   ```

3. **Verify:**
   - Next order created will have ID #1

## How It Works

### Database Support
- **SQLite**: Deletes entries from `sqlite_sequence` table
- **PostgreSQL**: Resets sequence using `ALTER SEQUENCE ... RESTART WITH 1`
- **MySQL**: Resets auto-increment using `ALTER TABLE ... AUTO_INCREMENT = 1`

### Safety Features
- Handles any remaining orders automatically
- Uses database transactions for data integrity
- Provides clear success/error messages
- Works for all related tables (Order, OrderItem, Payment)

## Example Output
```
Deleted 1 remaining orders
Successfully reset order ID sequence for SQLite
Order ID sequence has been reset. Next order will have ID 1.
```

## Testing
The functionality has been tested and verified:
- ✅ Order #1 created after reset
- ✅ All related tables (OrderItem, Payment) also reset
- ✅ Database integrity maintained
- ✅ Works after manual admin deletion

## Files Created
- `payment/management/commands/force_reset_orders.py` (RECOMMENDED)
- `payment/management/commands/reset_all_orders.py`
- `payment/management/commands/reset_order_sequence.py`
- `manual_reset.py` (standalone script)

## Quick Reference
**After deleting orders from admin:**
```bash
python manage.py force_reset_orders
```
**Next order will be #1** ✅
