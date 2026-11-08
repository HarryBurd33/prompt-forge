Create and save a real Excel workbook named `items_summary.xlsx` locally using the available file tools and bundled spreadsheet artifact library. Use the host’s recalculation and rendering capabilities. Do not upload to cloud services or substitute CSV.

The workbook must contain exactly two sheets, in this order: `Summary`, `Items`.

On `Items`, populate A1:D4 as follows, storing quantities and prices as numbers:

| Item | Quantity | Unit price | Line total |
|---|---:|---:|---|
| Notebook | 3 | 4.50 | =B2*C2 |
| Pen | 0 | 2.00 | =B3*C3 |
| Folder | 2 | 1.25 | =B4*C4 |

On `Summary`, set A1 to `Grand total` and B1 to `=SUM(Items!D2:D4)`. Preserve all formulas as live Excel formulas that update when inputs change. Retain the Pen quantity of zero as a valid numeric input and visibly display its zero line total.

Keep formatting simple and readable: bold headers, suitable column widths, integer quantities, and two decimal places for prices and totals. Do not add sheets or charts.

Before exporting the final workbook:

1. Verify every item, quantity, and price against the source table above. Independently compute expected results from those source inputs: line totals 13.50, 0.00, and 2.50; grand total 16.00. Recalculate and compare the workbook results with these expectations. Check that total cells contain formulas, not hardcoded results.
2. Temporarily change the Pen quantity in `Items!B3` from 0 to 2. Recalculate and verify that its line total becomes 4.00 and the summary grand total becomes 20.00. Restore B3 to numeric zero, recalculate again, and verify that the original totals return.
3. Render and visually inspect both sheets for readable text, visible zeros, correct number formatting, clipping, and formula errors. Correct any issues before export.

Export the restored, recalculated workbook as `.xlsx`. Reopen the saved file to confirm the two sheet names, source inputs, formulas, and calculated results survived export. If any required verification cannot be performed, state the limitation accurately instead of claiming success.

Return a link to the local workbook and a brief statement of the verification results.