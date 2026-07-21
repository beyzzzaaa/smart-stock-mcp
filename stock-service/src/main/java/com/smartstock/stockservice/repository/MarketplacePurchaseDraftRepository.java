package com.smartstock.stockservice.repository;

import com.smartstock.stockservice.model.MarketplacePurchaseDraft;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface MarketplacePurchaseDraftRepository extends JpaRepository<MarketplacePurchaseDraft, Long> {
}
