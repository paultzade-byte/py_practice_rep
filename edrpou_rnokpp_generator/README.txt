EDRPOU Generator & Validator
* **A simple Python script for generating and validating 8-digit EDRPOU codes according to Ukrainian state standards. Useful for QA engineers and developers for creating test data.

How the check digit calculation algorithm works:
The numerical value of the 7-digit base code is determined.

Depending on the range (e.g., [3_000_000; 6_000_000]), the appropriate array of weights is applied...

Calculation of the check digit for a 7-digit base code (without the check digit).

Algorithm (implemented according to public methodological guidelines):

Determine the numerical value of the 7-digit code (e.g., [4,1,5,6,4,4,5] -> 4156445).

If this value falls within the range [3_000_000; 6_000_000], the weights
[7, 1, 2, 3, 4, 5, 6] are used (the cycle is shifted by one position). Otherwise — weights [1, 2, 3, 4, 5, 6, 7].

Calculate S = sum(d_i * w_i) and r = S % 11.

If r != 10 → check digit = r.

If r == 10 → try alternative weight sequences: [3, 4, 5, 6, 7, 8, 9] and [9, 3, 4, 5, 6, 7, 8].

If r == 10 after alternative attempts → check digit = 0.

Note: this logic corresponds to the description provided in the methodological materials.
