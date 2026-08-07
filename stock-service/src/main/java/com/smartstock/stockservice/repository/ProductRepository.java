package com.smartstock.stockservice.repository;

import com.smartstock.stockservice.model.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    Optional<Product> findBySku(String sku);

    // List products where stock is exactly 0
    @Query("SELECT p FROM Product p WHERE p.stockQuantity = 0")
    List<Product> findOutOfStock();

    // List products where stock is less than or equal to minimum stock, but greater than 0
    @Query("SELECT p FROM Product p WHERE p.stockQuantity <= p.minimumStock AND p.stockQuantity > 0")
    List<Product> findLowStock();

    // Search by name, sku, description, subcategory name, or category name
    @Query("SELECT p FROM Product p WHERE " +
           "LOWER(p.name) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(p.sku) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(p.description) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(p.subcategory.name) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(p.subcategory.category.name) LIKE LOWER(CONCAT('%', :query, '%'))")
    List<Product> searchProducts(@Param("query") String query);

    // List all products that need replenishment (stock_quantity <= minimum_stock)
    @Query("SELECT p FROM Product p WHERE p.stockQuantity <= p.minimumStock")
    List<Product> findNeedsReplenishment();
}
