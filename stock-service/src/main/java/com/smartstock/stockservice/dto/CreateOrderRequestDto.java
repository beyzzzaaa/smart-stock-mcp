package com.smartstock.stockservice.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CreateOrderRequestDto {
    private Long productId;
    private Integer quantity;
    private LocalDateTime expectedDeliveryDate;
}
