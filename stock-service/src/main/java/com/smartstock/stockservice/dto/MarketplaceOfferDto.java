package com.smartstock.stockservice.dto;

import com.smartstock.stockservice.model.MarketplaceSeller;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class MarketplaceOfferDto {
    private Long id;
    private String productSku;
    private String productName;
    private MarketplaceSeller seller;
    private Double price;
    private Integer stockQuantity;
    private Double shippingFee;
    private Integer deliveryTimeDays;
    private Double topsisScore;
}
