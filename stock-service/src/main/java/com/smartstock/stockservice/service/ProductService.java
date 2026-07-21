package com.smartstock.stockservice.service;

import com.smartstock.stockservice.dto.ReplenishmentDto;
import com.smartstock.stockservice.model.Product;
import com.smartstock.stockservice.repository.IncomingOrderRepository;
import com.smartstock.stockservice.repository.ProductRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class ProductService {

    private final ProductRepository productRepository;
    private final IncomingOrderRepository incomingOrderRepository;

    public List<Product> getAllProducts() {
        return productRepository.findAll();
    }

    public Optional<Product> getProductById(Long id) {
        return productRepository.findById(id);
    }

    public Optional<Product> getProductBySku(String sku) {
        return productRepository.findBySku(sku);
    }

    public List<Product> getOutOfStockProducts() {
        return productRepository.findOutOfStock();
    }

    public List<Product> getLowStockProducts() {
        return productRepository.findLowStock();
    }

    public List<Product> searchProducts(String query) {
        return productRepository.searchProducts(query);
    }

    @Transactional
    public Product saveProduct(Product product) {
        return productRepository.save(product);
    }

    @Transactional
    public void deleteProduct(Long id) {
        productRepository.deleteById(id);
    }

    /**
     * Calculates replenishment needs for products that have stock levels at or below their minimum stock threshold.
     * Takes existing pending incoming orders into account.
     */
    public List<ReplenishmentDto> calculateReplenishment() {
        List<Product> needyProducts = productRepository.findNeedsReplenishment();
        
        return needyProducts.stream().map(product -> {
            Integer pendingQty = incomingOrderRepository.sumPendingQuantityByProduct(product);
            Integer needed = product.getTargetStock() - (product.getStockQuantity() + pendingQty);
            // Ensure we don't request negative values if target stock was exceeded or orders cover it
            int finalNeeded = Math.max(0, needed);
            
            return ReplenishmentDto.builder()
                    .productId(product.getId())
                    .sku(product.getSku())
                    .productName(product.getName())
                    .stockQuantity(product.getStockQuantity())
                    .minimumStock(product.getMinimumStock())
                    .targetStock(product.getTargetStock())
                    .pendingIncomingQuantity(pendingQty)
                    .replenishmentQuantityNeeded(finalNeeded)
                    .build();
        })
        .filter(dto -> dto.getReplenishmentQuantityNeeded() > 0) // Only return products that actually need more stock ordered
        .collect(Collectors.toList());
    }
}
