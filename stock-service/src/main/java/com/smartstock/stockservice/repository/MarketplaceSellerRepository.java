package com.smartstock.stockservice.repository;

import com.smartstock.stockservice.model.MarketplaceSeller;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface MarketplaceSellerRepository extends JpaRepository<MarketplaceSeller, Long> {
    Optional<MarketplaceSeller> findByName(String name);
}
