# Mosel Data Format Specification

This document describes the Mosel `.dat` file format used for MCLP instances.

## 📋 Overview

The Mosel data format is a text-based format that defines:
- Problem dimensions (number of facilities, customers)
- Facility costs and customer demands
- Coverage relationships between facilities and customers
- Budget constraint

## 📝 File Structure

Each `.dat` file contains the following sections in order:

```
! === SCALARS ===
nI: <number_of_facilities>
nJ: <number_of_customers>
BUDGET: <budget_value>

! === FACILITY INDICES ===
FACILITIES: [<space-separated facility IDs>]

! === CUSTOMER INDICES ===
CUSTOMERS: [<space-separated customer IDs>]

! === FACILITY COSTS ===
COST: [
  <facility_id> <cost_value>
  ...
]

! === CUSTOMER DEMANDS ===
DEMAND: [
  <customer_id> <demand_value>
  ...
]

! === COVERAGE SETS I_j ===
COVERAGE_I_j: [
  <customer_id> [<facilities that can cover this customer>]
  ...
]

! === REVERSE COVERAGE SETS J_i ===
COVERAGE_J_i: [
  <facility_id> [<customers covered by this facility>]
  ...
]
```

## 🔍 Detailed Section Descriptions

### 1. Scalars

Defines problem dimensions and budget:

```mosel
nI: 4          ! Number of facilities
nJ: 8          ! Number of customers
BUDGET: 5.0    ! Total budget available
```

**Usage in Mosel**:
```mosel
declarations
  nI, nJ: integer
  BUDGET: real
end-declarations

initializations from "data/instance.dat"
  nI nJ BUDGET
end-initializations
```

### 2. Facility Indices

List of facility IDs (typically 0-indexed):

```mosel
FACILITIES: [0 1 2 3]
```

**Usage in Mosel**:
```mosel
declarations
  FACILITIES: set of integer
end-declarations

initializations from "data/instance.dat"
  FACILITIES
end-initializations
```

### 3. Customer Indices

List of customer IDs (typically 0-indexed):

```mosel
CUSTOMERS: [0 1 2 3 4 5 6 7]
```

**Usage in Mosel**:
```mosel
declarations
  CUSTOMERS: set of integer
end-declarations

initializations from "data/instance.dat"
  CUSTOMERS
end-initializations
```

### 4. Facility Costs

Cost to open each facility:

```mosel
COST: [
  0 2.000000    ! Facility 0 costs 2.0
  1 3.000000    ! Facility 1 costs 3.0
  2 2.500000    ! Facility 2 costs 2.5
  3 1.500000    ! Facility 3 costs 1.5
]
```

**Usage in Mosel**:
```mosel
declarations
  COST: array(FACILITIES) of real
end-declarations

initializations from "data/instance.dat"
  COST
end-initializations
```

### 5. Customer Demands

Demand value for each customer:

```mosel
DEMAND: [
  0 10.000000   ! Customer 0 has demand 10.0
  1 15.000000   ! Customer 1 has demand 15.0
  ...
]
```

**Usage in Mosel**:
```mosel
declarations
  DEMAND: array(CUSTOMERS) of real
end-declarations

initializations from "data/instance.dat"
  DEMAND
end-initializations
```

### 6. Coverage Sets I_j

For each customer, lists which facilities can cover it:

```mosel
COVERAGE_I_j: [
  0 [0 1]       ! Customer 0 can be covered by facilities 0, 1
  1 [1 2]       ! Customer 1 can be covered by facilities 1, 2
  2 [2]         ! Customer 2 can only be covered by facility 2
  3 [0 3]       ! Customer 3 can be covered by facilities 0, 3
  ...
]
```

**Usage in Mosel**:
```mosel
declarations
  I_j: array(CUSTOMERS) of set of integer
end-declarations

initializations from "data/instance.dat"
  I_j as "COVERAGE_I_j"
end-initializations

! Example: Check if facility 1 can cover customer 0
if 1 in I_j(0) then
  writeln("Facility 1 can cover customer 0")
end-if
```

### 7. Reverse Coverage Sets J_i

For each facility, lists which customers it can cover:

```mosel
COVERAGE_J_i: [
  0 [0 3 6]     ! Facility 0 covers customers 0, 3, 6
  1 [0 1 4 7]   ! Facility 1 covers customers 0, 1, 4, 7
  2 [1 2 5 6]   ! Facility 2 covers customers 1, 2, 5, 6
  3 [3 4 5 7]   ! Facility 3 covers customers 3, 4, 5, 7
]
```

**Usage in Mosel**:
```mosel
declarations
  J_i: array(FACILITIES) of set of integer
end-declarations

initializations from "data/instance.dat"
  J_i as "COVERAGE_J_i"
end-initializations

! Example: Iterate over customers covered by facility 0
forall(j in J_i(0))
  writeln("Facility 0 covers customer ", j)
end-forall
```

## 💡 Complete Mosel Loading Example

Here's a complete example of loading a `.dat` file in Mosel:

```mosel
model "LoadMCLPInstance"
  uses "mmxprs"

  ! Forward declarations
  declarations
    nI, nJ: integer
    BUDGET: real
  end-declarations

  ! Load dimensions first
  initializations from "data/test_tiny.dat"
    nI nJ BUDGET
  end-initializations

  ! Now declare arrays with proper dimensions
  declarations
    FACILITIES: set of integer
    CUSTOMERS: set of integer
    COST: array(0..nI-1) of real
    DEMAND: array(0..nJ-1) of real
    I_j: array(0..nJ-1) of set of integer
    J_i: array(0..nI-1) of set of integer
  end-declarations

  ! Load the rest of the data
  initializations from "data/test_tiny.dat"
    FACILITIES CUSTOMERS
    COST DEMAND
    I_j as "COVERAGE_I_j"
    J_i as "COVERAGE_J_i"
  end-initializations

  ! Validate data
  writeln("Instance loaded successfully!")
  writeln("Facilities: ", nI, ", Customers: ", nJ)
  writeln("Budget: ", BUDGET)

  ! Example: Print coverage information
  forall(j in CUSTOMERS) do
    write("Customer ", j, " can be covered by facilities: ")
    forall(i in I_j(j))
      write(i, " ")
    writeln("")
  end-forall

end-model
```

## 📊 Data Validation Rules

When reading `.dat` files, validate:

1. **Consistency**: Every arc in I_j must have corresponding arc in J_i
   ```mosel
   ! Check: if i ∈ I_j(j), then j ∈ J_i(i)
   forall(j in CUSTOMERS, i in I_j(j))
     assert(j in J_i(i), "Coverage matrix inconsistency detected")
   ```

2. **Feasibility**: At least one facility can cover each customer
   ```mosel
   forall(j in CUSTOMERS)
     assert(card(I_j(j)) > 0, "Customer " + j + " has no covering facilities")
   ```

3. **Budget**: Budget must be positive and allow opening at least one facility
   ```mosel
   min_cost := min(i in FACILITIES) COST(i)
   assert(BUDGET >= min_cost, "Budget too small to open any facility")
   ```

4. **Non-negativity**: All costs and demands must be non-negative
   ```mosel
   forall(i in FACILITIES)
     assert(COST(i) >= 0, "Negative facility cost detected")
   forall(j in CUSTOMERS)
     assert(DEMAND(j) >= 0, "Negative customer demand detected")
   ```

## 🔄 Conversion from JSON

The Python utility `convert_json_to_mosel.py` converts JSON to this format:

**JSON Structure (Input)**:
```json
{
  "name": "test_tiny",
  "I": [0, 1, 2, 3],
  "J": [0, 1, 2, 3, 4, 5, 6, 7],
  "f": {"0": 2.0, "1": 3.0, "2": 2.5, "3": 1.5},
  "d": {"0": 10, "1": 15, "2": 20, ...},
  "I_j": {"0": [0, 1], "1": [1, 2], ...},
  "B": 5.0
}
```

**Mosel .dat (Output)**:
```mosel
nI: 4
nJ: 8
BUDGET: 5.0
FACILITIES: [0 1 2 3]
CUSTOMERS: [0 1 2 3 4 5 6 7]
COST: [0 2.0, 1 3.0, ...]
...
```

### Running Conversion

```bash
python utilities/convert_json_to_mosel.py \
  --input-dir ../data/ \
  --output-dir data/
```

## 🎯 Example: test_tiny.dat

Complete example of smallest instance:

```mosel
! MCLP Instance: test_tiny
! Generated from: test_tiny.json
! Facilities: 4, Customers: 8
! Budget: 5.00

! === SCALARS ===
nI: 4
nJ: 8
BUDGET: 5.0

! === FACILITY INDICES ===
FACILITIES: [0 1 2 3]

! === CUSTOMER INDICES ===
CUSTOMERS: [0 1 2 3 4 5 6 7]

! === FACILITY COSTS ===
COST: [
  0 2.000000
  1 3.000000
  2 2.500000
  3 1.500000
]

! === CUSTOMER DEMANDS ===
DEMAND: [
  0 10.000000
  1 15.000000
  2 20.000000
  3 25.000000
  4 30.000000
  5 12.000000
  6 18.000000
  7 22.000000
]

! === COVERAGE SETS I_j ===
COVERAGE_I_j: [
  0 [0 1]
  1 [1 2]
  2 [2]
  3 [0 3]
  4 [1 3]
  5 [2 3]
  6 [0 2]
  7 [1 3]
]

! === REVERSE COVERAGE SETS J_i ===
COVERAGE_J_i: [
  0 [0 3 6]
  1 [0 1 4 7]
  2 [1 2 5 6]
  3 [3 4 5 7]
]
```

## 📏 Instance Size Reference

| Instance  | nI  | nJ   | File Size | Load Time* |
|-----------|-----|------|-----------|------------|
| test_tiny | 4   | 8    | 1.1 KB    | <0.01s     |
| S1        | 50  | 200  | 16 KB     | <0.1s      |
| S2        | 50  | 200  | 16 KB     | <0.1s      |
| M1        | 100 | 500  | 55 KB     | ~0.2s      |
| M2        | 100 | 500  | 55 KB     | ~0.2s      |
| L1        | 200 | 1000 | 158 KB    | ~0.5s      |
| L2        | 200 | 1000 | 139 KB    | ~0.5s      |

*Approximate Mosel load times on standard hardware

## ⚠️ Common Issues

### Issue: "Index out of range"

**Cause**: Mosel arrays are 1-indexed by default, but our data uses 0-indexed IDs

**Solution**: Declare arrays with explicit 0-based indexing:
```mosel
declarations
  COST: array(0..nI-1) of real  ! NOT array(FACILITIES)
end-declarations
```

### Issue: "Set initialization failed"

**Cause**: Mismatch between declaration name and data file name

**Solution**: Use `as` keyword to map names:
```mosel
initializations from "data/instance.dat"
  I_j as "COVERAGE_I_j"  ! Map I_j variable to COVERAGE_I_j in file
end-initializations
```

### Issue: "Coverage matrix incomplete"

**Cause**: Not loading both I_j and J_i

**Solution**: Load both coverage directions (needed for efficient algorithms):
```mosel
initializations from "data/instance.dat"
  I_j as "COVERAGE_I_j"
  J_i as "COVERAGE_J_i"
end-initializations
```

## 🚀 Best Practices

1. **Always validate after loading**: Check consistency, feasibility, non-negativity
2. **Use meaningful variable names**: Match mathematical notation (I_j, J_i)
3. **Comment data files**: Include instance statistics as comments
4. **Version control**: Track changes to data format with git
5. **Modular loading**: Separate data loading into reusable initialization block

---

**Updated**: November 21, 2025
**Author**: MCLP Migration Team
