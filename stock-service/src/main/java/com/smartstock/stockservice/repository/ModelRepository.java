package com.smartstock.stockservice.repository;

import com.smartstock.stockservice.model.Brand;
import com.smartstock.stockservice.model.Model;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface ModelRepository extends JpaRepository<Model, Long> {
    List<Model> findByBrand(Brand brand);
    Optional<Model> findByBrandAndName(Brand brand, String name);
}
