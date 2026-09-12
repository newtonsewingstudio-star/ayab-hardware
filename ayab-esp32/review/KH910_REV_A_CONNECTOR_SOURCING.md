# KH910 Rev A — Machine Connector Sourcing and Assembly Control

Status: controlled procurement record for the one-off KH910 Rev A prototype. Stock observations are dated and must be rechecked at order time. Native KiCad fields and the manufacturing metadata validator remain authoritative for reference designators, footprints, and exact manufacturer part numbers.

Last supplier check: 2026-09-12

## Required KH910 connector population

| References | Qty/board | Manufacturer | Exact MPN | Finish | Board footprint |
|---|---:|---|---|---|---|
| J403, J405 | 2 | Hirose | `HNC2-2.5P-10DS(02)` | Gold | `Library:HNC2-2.5P-10DS` |
| J404 | 1 | Hirose | `HNC2-2.5P-8DS(02)` | Gold | `Library:HNC2-2.5P-8DS` |
| J408 | 1 | Hirose | `HNC2-2.5P-3DS(02)` | Gold | `Library:HNC2-2.5P-3DS` |

J406 is for other Brother machine variants and is not fitted for the KH910 prototype. Generic 2.5 mm headers are not approved substitutes: pitch alone does not establish the required housing geometry, polarization, lock, contact position, or machine-harness fit.

For one prototype, procure at least two fitted sets when practical: four 10-position headers, two 8-position headers, and two 3-position headers. The second set is a handling/rework spare, not an additional board population. If an assembler requires a different attrition quantity, obtain that quantity in writing before purchasing or consigning parts.

## Preferred sources observed on 2026-09-12

| Exact MPN | Preferred source | Observed status | Procurement note |
|---|---|---|---|
| `HNC2-2.5P-10DS(02)` | [Mouser 798-HNC22.5P10DS02](https://www.mouser.es/en/ProductDetail/Hirose-Connector/HNC2-25P-10DS02?qs=gyfFsMMHMKwKipyRCQFxxQ%3D%3D) | 398 pieces shown in stock; discontinued | Buy exact new-old stock while traceable inventory remains. Two are fitted per board. |
| `HNC2-2.5P-8DS(02)` | [Furutaka Parts Online](https://www.furutaka-netsel.co.jp/maker/hrs/hnc2-2.5p-8ds_02) | Listed as in stock at JPY 80 before tax | Confirm export/shipping availability and exact `(02)` suffix before payment. |
| `HNC2-2.5P-3DS(02)` | [DigiKey H126245-ND](https://www.digikey.com/en/products/detail/hirose-electric-co-ltd/HNC2-2-5P-3DS-02/4284914) | Active; 669 pieces shown in stock at USD 0.88 each | Preferred authorized-distributor source for J408. |

Hirose's [HNC series page](https://www.hirose.com/en/product/series/HNC) and [series catalog](https://www.mouser.com/datasheet/2/185/HNC_2_5S_C_A_252815_2529_CL0218_0021_5_15_Catalog_-2492144.pdf) are the identity and mechanical references. Distributor inventory and prices are volatile and are not design guarantees.

## Substitution control

`HNC2-2.5P-10DS(55)` and `HNC2-2.5P-8DS(55)` are same-series, same-position-count tin-finish parts that appear to share the required board geometry. They are **not approved substitutions** for this first article. The machine-side female contact finish has not been physically verified, and mixing gold and tin at a separable contact interface can reduce long-term reliability.

No substitute may be accepted from a distributor or assembler solely because it is described as a 2.5 mm header or a parametric equivalent. A proposed substitute requires a documented comparison of the manufacturer drawing, pin numbering, polarization/keying, latch geometry, body envelope, board drill pattern, current rating, and both mating contact finishes, followed by a new mechanical/electrical review.

## Manufacturer-installation route

JLCPCB states that it can source non-library parts through Global Sourcing or a New Parts Request, accept customer-consigned parts, and manually assemble through-hole connectors. Therefore all four KH910 connectors can in principle be installed by JLCPCB, but only after the exact MPNs are present in the customer's private parts library and explicitly matched in the assembly order.

Preferred order of operations:

1. Submit a JLCPCB New Parts Request or Global Sourcing request for the three exact Hirose MPNs above. This is the preferred turnkey route if JLCPCB confirms the exact suffix, quantity, and through-hole assembly service.
2. If JLCPCB cannot source them, compare its current overseas-consignment fees, customs process, attrition requirement, and lead time with local post-assembly installation. Consignment is supported, but it may be disproportionately expensive and administratively heavy for four connector types on one prototype.
3. If the manufacturer does not install them, order the assembled PCB with J403/J404/J405/J408 deliberately unpopulated and have a qualified local assembler hand-solder the exact parts. Inspect part identity, seating, orientation, solder fill, bridges, and mechanical alignment before connecting the machine harness.

Relevant JLCPCB instructions:

- [PCBA parts sourcing options](https://jlcpcb.com/help/article/pcba-parts-sourcing-instruction)
- [Using private/global/consigned parts in an assembly order](https://jlcpcb.com/help/article/how-to-use-my-own-parts-for-pcb-assembly-order)
- [Consignment terms](https://jlcpcb.com/help/article/consignment-part-terms-conditions)
- [Through-hole assembly support](https://jlcpcb.com/help/article/pcb-assembly-faqs)

## Assembly-data release rule

The controlled engineering BOM already includes J403/J404/J405/J408 with the exact MPNs, and the PCB already contains their correct through-hole footprints. The default automated JLC BOM intentionally omits parts that have no confirmed JLC/LCSC identifier. Do not invent an identifier or allow an automatic match.

Before a manufacturer-install order is released, preserve the existing controlled fabrication data and create an order-specific assembly BOM/CPL from the same source commit in which:

- the exact JLC private/global/consigned part identifier is recorded for each of J403/J404/J405/J408;
- every reference is explicitly selected in the component-matching screen;
- orientation is checked against the native KiCad board and connector pin 1;
- no substitution is enabled for these references; and
- the manufacturer's reviewed component-match summary is saved with the order record.

If these conditions cannot be met, the four connectors remain a controlled post-assembly operation. Their absence from automated assembly is acceptable only when it is explicit; a supposedly complete board with an unreviewed connector substitution is not acceptable.
