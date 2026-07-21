package com.smartstock.stockservice.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "marketplace_purchase_draft_items")
public class MarketplacePurchaseDraftItem {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "draft_id", nullable = false)
    private MarketplacePurchaseDraft draft;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "product_id", nullable = false)
    private Product product;

    @Column(nullable = false)
    private Integer quantity;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "seller_id", nullable = false)
    private MarketplaceSeller seller;

    @Column(nullable = false)
    private Double price;

    @Column(name = "shipping_fee", nullable = false)
    private Double shippingFee;

    @Column(name = "delivery_time_days", nullable = false)
    private Integer deliveryTimeDays;
}
