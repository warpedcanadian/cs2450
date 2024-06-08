| Test Name                  | Description                              | Use Case                | Inputs                          | Expected Outputs               | Success Criteria                        |
|----------------------------|------------------------------------------|-------------------------|---------------------------------|---------------------------------|-----------------------------------------|
| test_read_success          | Test successful READ operation           | READ Operation          | Input: '1001'                   | Memory[1]: 1001                 | Memory[1] is 1001                       |
| test_write_success         | Test successful WRITE operation          | WRITE Operation         | Memory[0]: 1234                 | Output: '1234'                  | Output contains '1234'                  |
| test_load_success          | Test successful LOAD operation           | LOAD Operation          | Memory[0]: 2000                 | Accumulator: 2000               | Accumulator is 2000                     |
| test_store_success         | Test successful STORE operation          | STORE Operation         | Accumulator: 1234               | Memory[0]: 1234                 | Memory[0] is 1234                       |
| test_add_success           | Test successful ADD operation            | ADD Operation           | Memory[0]: 1723, Memory[1]: 3001| Accumulator: 5001               | Accumulator is 5001                     |
| test_subtract_success      | Test successful SUBTRACT operation       | SUBTRACT Operation      | Memory[0]: 1000, Memory[1]: 1001| Accumulator: 1                  | Accumulator is 1                        |
| test_divide_success        | Test successful DIVIDE operation         | DIVIDE Operation        | Memory[0]: 1000, Memory[1]: 2000| Accumulator: 1                  | Accumulator is 1                        |
| test_multiply_success      | Test successful MULTIPLY operation       | MULTIPLY Operation      | Memory[0]: 1000, Memory[1]: 2000| Accumulator: 1000000            | Accumulator is 1000000                  |
| test_branch_success        | Test successful BRANCH operation         | BRANCH Operation        | Memory[1]: 5678                 | Output: '5678'                  | Output contains '5678'                  |
| test_branchneg_success     | Test successful BRANCHNEG operation      | BRANCHNEG Operation     | Memory[0]: -1, Memory[2]: 9999  | Output: '9999'                  | Output contains '9999'                  |
| test_branchzero_success    | Test successful BRANCHZERO operation     | BRANCHZERO Operation    | Memory[0]: 0, Memory[2]: 9999   | Output: '9999'                  | Output contains '9999'                  |
| test_halt_success          | Test successful HALT operation           | HALT Operation          | None                            | Running: False                  | `self.running` is False                 |