package com.smartstock.stockservice.dto;

import com.smartstock.stockservice.model.MarketplaceSeller;
import com.smartstock.stockservice.model.Product;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class MarketplaceOrderItemResponseDto {
    private Long id;
    private Product product;
    private Integer quantity;
    private MarketplaceSeller seller;
    private Double price;
    private Double shippingFee;
    private Integer deliveryTimeDays;
}
