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
        if (query == null || query.isBlank()) {
            return List.of();
        }
        String[] terms = query.trim().split("\\s+");
        List<Product> all = productRepository.findAll();
        return all.stream().filter(p -> {
            for (String term : terms) {
                String lowerTerm = term.toLowerCase();
                boolean match = (p.getName() != null && p.getName().toLowerCase().contains(lowerTerm)) ||
                                (p.getSku() != null && p.getSku().toLowerCase().contains(lowerTerm)) ||
                                (p.getDescription() != null && p.getDescription().toLowerCase().contains(lowerTerm)) ||
                                (p.getSubcategory() != null && p.getSubcategory().getName() != null && p.getSubcategory().getName().toLowerCase().contains(lowerTerm)) ||
                                (p.getSubcategory() != null && p.getSubcategory().getCategory() != null && p.getSubcategory().getCategory().getName() != null && p.getSubcategory().getCategory().getName().toLowerCase().contains(lowerTerm)) ||
                                (p.getModel() != null && p.getModel().getName() != null && p.getModel().getName().toLowerCase().contains(lowerTerm)) ||
                                (p.getModel() != null && p.getModel().getBrand() != null && p.getModel().getBrand().getName() != null && p.getModel().getBrand().getName().toLowerCase().contains(lowerTerm));
                if (!match) {
                    return false;
                }
            }
            return true;
        }).collect(Collectors.toList());
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
    public List<ReplenishmentDto> calculateReplenishment(List<Long> productIds) {
        List<Product> needyProducts;
        if (productIds == null || productIds.isEmpty()) {
            needyProducts = productRepository.findNeedsReplenishment();
        } else {
            needyProducts = productRepository.findAllById(productIds);
        }
        
        return needyProducts.stream().map(product -> {
            Integer pendingQty = incomingOrderRepository.sumPendingQuantityByProduct(product);
            Integer needed = product.getTargetStock() - (product.getStockQuantity() + pendingQty);
            // Ensure we don't request negative values if target stock was exceeded or orders cover it
            int finalNeeded = Math.max(0, needed);
            
            String categoryName = null;
            if (product.getSubcategory() != null && product.getSubcategory().getCategory() != null) {
                categoryName = product.getSubcategory().getCategory().getName();
            }
            
            return ReplenishmentDto.builder()
                    .productId(product.getId())
                    .sku(product.getSku())
                    .productName(product.getName())
                    .categoryName(categoryName)
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
