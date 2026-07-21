package com.smartstock.stockservice.repository;

import com.smartstock.stockservice.model.IncomingOrder;
import com.smartstock.stockservice.model.IncomingOrderStatus;
import com.smartstock.stockservice.model.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface IncomingOrderRepository extends JpaRepository<IncomingOrder, Long> {
    List<IncomingOrder> findByStatus(IncomingOrderStatus status);

    List<IncomingOrder> findByProductAndStatus(Product product, IncomingOrderStatus status);

    // Sum of quantity of pending orders for a specific product
    @Query("SELECT COALESCE(SUM(o.quantity), 0) FROM IncomingOrder o WHERE o.product = :product AND o.status = 'PENDING'")
    Integer sumPendingQuantityByProduct(@Param("product") Product product);
}
