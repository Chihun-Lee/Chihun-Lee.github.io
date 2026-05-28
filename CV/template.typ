// Academic CV template — Typst 0.14
// Single column, A4, serif body. Generated from YAML SSOT by build_cv.py.

#let serif = ("Libertinus Serif", "Source Serif 4", "New Computer Modern", "Times New Roman")
#let sans  = ("Libertinus Sans", "Source Sans 3", "Inter", "Helvetica")

#let cv(
  name: "",
  title: "",
  affiliation: "",
  division: "",
  contact_line: "",
  links_line: "",
  body
) = {
  set page(
    paper: "a4",
    margin: (x: 2cm, y: 2cm),
    footer: context [
      #set align(center)
      #set text(size: 8pt, fill: rgb("#666666"))
      #counter(page).display("1 / 1", both: true)
    ],
  )
  set text(font: serif, size: 10pt, lang: "en")
  set par(justify: true, leading: 0.55em)

  // ── Header ─────────────────────────────────────────────────
  align(left)[
    #text(size: 22pt, weight: "bold")[#name] \
    #text(size: 10.5pt, style: "italic")[#title] \
    #text(size: 10pt)[#affiliation#if division != "" [, #division]] \
    #text(size: 9pt, fill: rgb("#333333"))[#contact_line] \
    #if links_line != "" [#text(size: 9pt, fill: rgb("#333333"))[#links_line]]
  ]
  v(0.4em)
  line(length: 100%, stroke: 0.6pt + rgb("#333333"))
  v(0.2em)

  body
}

#let section(title) = {
  v(0.6em)
  text(size: 11pt, weight: "bold", tracking: 0.08em, upper(title))
  v(-0.2em)
  line(length: 100%, stroke: 0.4pt + rgb("#999999"))
  v(0.2em)
}

#let entry(lhs, rhs) = {
  grid(
    columns: (1fr, auto),
    column-gutter: 1em,
    lhs, align(right)[#text(fill: rgb("#444444"))[#rhs]]
  )
}

// Numbered item — N is right-aligned in a narrow gutter
#let item(n, body) = {
  grid(
    columns: (1.6em, 1fr),
    column-gutter: 0.4em,
    align(right)[#text(fill: rgb("#666666"))[\[#n\]]],
    body,
  )
  v(0.25em)
}
