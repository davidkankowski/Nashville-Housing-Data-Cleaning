-- CREATE DATABASE PortfolioProject;
-- ALTER DATABASE PortfolioProject SET RECOVERY SIMPLE;
USE PortfolioProject;

-------------------------------------------------------------------------

-- Cleaning Data in SQL Queries

Select *
From PortfolioProject.dbo.NashvilleHousing

-------------------------------------------------------------------------

-- Standardize Date Format

Select SaleDateConverted, CONVERT(Date,SaleDate)
From PortfolioProject.dbo.NashvilleHousing

Update NashvilleHousing
SET SaleDate = CONVERT(Date,SaleDate)

ALTER TABLE NashvilleHousing
Add SaleDateConverted Date;

Update NashvilleHousing
SET SaleDateConverted = CONVERT(Date,SaleDate)

-------------------------------------------------------------------------