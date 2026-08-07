package com.smartstock.stockservice.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ReplenishmentDto {
    private Long productId;
    private String sku;
    private String productName;
    private String categoryName;
    private Integer stockQuantity;
    private Integer minimumStock;
    private Integer targetStock;
    private Integer pendingIncomingQuantity;
    private Integer replenishmentQuantityNeeded;
}
