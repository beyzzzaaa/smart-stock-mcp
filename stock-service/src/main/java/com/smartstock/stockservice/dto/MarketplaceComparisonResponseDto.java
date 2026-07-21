package com.smartstock.stockservice.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class MarketplaceComparisonResponseDto {
    private List<MarketplaceOfferDto> offers;
    private MarketplaceOfferDto bestChoice;
}
