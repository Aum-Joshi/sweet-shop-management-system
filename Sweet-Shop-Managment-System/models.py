"""
Data models for Sweet Shop Management System

This module defines the data structures used by the application.
Since we're using a simple in-memory storage approach, these models
are primarily for documentation and potential future database integration.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict
from datetime import datetime


@dataclass
class SweetModel:
    """Data model for a sweet item."""
    id: str
    name: str
    category: str
    price: float
    quantity: int
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        """Set timestamps if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


@dataclass
class PurchaseRecord:
    """Data model for a purchase transaction."""
    id: str
    sweet_id: str
    sweet_name: str
    quantity: int
    unit_price: float
    total_cost: float
    timestamp: datetime = None
    
    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class RestockRecord:
    """Data model for a restock transaction."""
    id: str
    sweet_id: str
    sweet_name: str
    quantity_added: int
    previous_stock: int
    new_stock: int
    timestamp: datetime = None
    
    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()


class ShopStatistics:
    """Class to calculate and store shop statistics."""
    
    def __init__(self, sweets: List[Dict]):
        """Initialize with current sweets data."""
        self.sweets = sweets
        self._calculate_stats()
    
    def _calculate_stats(self):
        """Calculate various statistics."""
        if not self.sweets:
            self.total_items = 0
            self.total_categories = 0
            self.total_value = 0.0
            self.average_price = 0.0
            self.low_stock_count = 0
            self.categories = []
            return
        
        self.total_items = len(self.sweets)
        self.categories = list(set(sweet['category'] for sweet in self.sweets))
        self.total_categories = len(self.categories)
        self.total_value = sum(sweet['price'] * sweet['quantity'] for sweet in self.sweets)
        self.average_price = sum(sweet['price'] for sweet in self.sweets) / self.total_items
        self.low_stock_count = len([s for s in self.sweets if s['quantity'] <= 5])
    
    def to_dict(self) -> Dict:
        """Convert statistics to dictionary."""
        return {
            'total_items': self.total_items,
            'total_categories': self.total_categories,
            'total_value': self.total_value,
            'average_price': round(self.average_price, 2),
            'low_stock_count': self.low_stock_count,
            'categories': self.categories
        }


# Category constants for validation
SWEET_CATEGORIES = [
    'Chocolate',
    'Candy',
    'Pastry',
    'Nut-Based',
    'Milk-Based',
    'Vegetable-Based',
    'Syrup-Based',
    'Fruit-Based',
    'Ice Cream',
    'Cookies',
    'Other'
]

# Validation functions
def validate_sweet_name(name: str) -> bool:
    """Validate sweet name."""
    return isinstance(name, str) and len(name.strip()) > 0

def validate_sweet_category(category: str) -> bool:
    """Validate sweet category."""
    return isinstance(category, str) and len(category.strip()) > 0

def validate_sweet_price(price: float) -> bool:
    """Validate sweet price."""
    return isinstance(price, (int, float)) and price > 0

def validate_sweet_quantity(quantity: int) -> bool:
    """Validate sweet quantity."""
    return isinstance(quantity, int) and quantity >= 0
