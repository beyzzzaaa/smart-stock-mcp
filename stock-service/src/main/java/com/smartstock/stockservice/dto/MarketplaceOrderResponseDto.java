package com.smartstock.stockservice.dto;

import com.smartstock.stockservice.model.MarketplaceOrderStatus;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class MarketplaceOrderResponseDto {
    private Long id;
    private Long draftId;
    private Double totalCost;
    private MarketplaceOrderStatus status;
    private LocalDateTime createdAt;
    private LocalDateTime expectedDeliveryDate;
    private List<MarketplaceOrderItemResponseDto> items;
}
