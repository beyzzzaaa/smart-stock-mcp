package com.smartstock.stockservice.repository;

import com.smartstock.stockservice.model.MarketplaceOffer;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface MarketplaceOfferRepository extends JpaRepository<MarketplaceOffer, Long> {
    List<MarketplaceOffer> findByProductSku(String sku);

    List<MarketplaceOffer> findByProductId(Long productId);

    Optional<MarketplaceOffer> findByProductSkuAndSellerId(String sku, Long sellerId);

    @Query("SELECT o FROM MarketplaceOffer o WHERE " +
           "LOWER(o.product.sku) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(o.product.name) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(o.seller.name) LIKE LOWER(CONCAT('%', :query, '%'))")
    List<MarketplaceOffer> searchOffers(@Param("query") String query);
}
