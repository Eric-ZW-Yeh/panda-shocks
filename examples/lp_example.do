* Panel local projection of an outcome on the soft-power shock (SPS, z_birth_nat) (Stata 15+).
*   y_{i,t+h} - y_{i,t-1} = a_i + l_t + b_h * z_{i,t} + e_{i,t+h},  h = 0..24
* z = z_birth_nat; host and month fixed effects; SE clustered by month; sample 2011-01 onward.
* Needs: ssc install reghdfe ftools
* Input: my_outcome.csv with columns host, month (YYYY-MM), y. Run from the repository root.

clear all
set more off
local H = 24

import delimited using "my_outcome.csv", varnames(1) stringcols(1 2) clear
tempfile y
save `y'

import delimited using "data/panda_shocks_monthly.csv", varnames(1) stringcols(1 2) clear
merge 1:1 host month using `y', keep(match) nogenerate

gen mdate = monthly(month, "YM")
format mdate %tm
encode host, gen(hid)
xtset hid mdate

tempname R
postfile `R' h b se using "lp_results.dta", replace
forvalues h = 0/`H' {
    quietly gen dy = F`h'.y - L.y
    quietly reghdfe dy z_birth_nat if mdate >= tm(2011m1), absorb(hid mdate) vce(cluster mdate)
    post `R' (`h') (_b[z_birth_nat]) (_se[z_birth_nat])
    drop dy
}
postclose `R'

use "lp_results.dta", clear
gen lo90 = b - 1.645*se
gen hi90 = b + 1.645*se
gen lo68 = b - se
gen hi68 = b + se
twoway (rarea lo90 hi90 h, color("31 45 92%15") lwidth(none)) ///
       (rarea lo68 hi68 h, color("31 45 92%35") lwidth(none)) ///
       (line b h, lcolor("31 45 92") lwidth(medthick)), ///
       yline(0, lcolor(black)) legend(off) graphregion(color(white)) ///
       xtitle("months after the birth announcement") ytitle("response per unit of z")
graph export "lp_example_stata.png", replace width(1200)
list h b se, noobs clean
