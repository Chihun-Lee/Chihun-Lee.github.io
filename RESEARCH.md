# Research Achievements — Chihun Lee, Ph.D.

> *Senior Researcher, Material Data & Analysis Research Division*
> *Korea Institute of Materials Science (KIMS)*
>
> Derived from `data/*.yaml` — last updated **2026-05-28**.
> See [`data/publications.yaml`](data/publications.yaml), [`data/projects.yaml`](data/projects.yaml), [`data/talks.yaml`](data/talks.yaml), [`data/patents.yaml`](data/patents.yaml).

---

## At a Glance

| | |
|---|---|
| **Total citations** | **733** |
| **h-index** | **12** |
| **i10-index** | **12** |
| **Peer-reviewed publications** | **23** (9 first-author / 14 co-author) |
| **Patents** | **5** (1 PCT, 4 Korea) |
| **Conference talks** | **11** (7 international / 4 domestic) |
| **Industry / national projects** | **8** |
| **Equal-contribution papers** | **10** |

---

## Research Map

I work at the intersection of optimization, machine learning, and physical sciences across **four interconnected pillars**. Each pillar feeds the next: manufacturing process data trains models that inform nanophotonic inverse design, while materials science grounds the autonomous metal laboratory that closes the loop back to manufacturing.

```mermaid
mindmap
  root((Chihun Lee<br/>AI × Optimization × Physics))
    Manufacturing Optimization
      Injection molding
      Hot-rolled coil placement
      Punch press / drilling
      Powder injection molding
      Process–property models
    Nanophotonics Optimization
      Metasurface inverse design
      Achromatic metalens
      Meta-hologram
      Color filter
      3D nanopatterning mask
      OLED beam control
      Transmissive antenna
    Materials Optimization
      Fe-C / Fe-C-Cu compaction
      316L stainless powder rheology
      Dual-phase steel microstructure
      Constitutive + ANN hybrids
    Metal Autonomous Laboratory
      Laser powder bed fusion
      Bayesian optimization
      Active learning loops
      Sim-experiment coupling
```

---

## Pillar 1 — Manufacturing Optimization (제조 최적화)

> Data-driven and physics-informed optimization for industrial manufacturing.
> *Industry partners: POSCO, LG Display, LS mtron, Samsung Display, KITECH.*

**Core publications**

| Year | Title | Venue | Role |
|------|-------|-------|------|
| 2025 | Real-Time Hot-Rolled Coil Placement Recommendation System with Data-Driven Model | *Advanced Intelligent Systems* | **First** (POSCO) |
| 2022 | Mass production of superhydrophilic micropatterned copper surfaces using powder injection molding process | *Powder Technology* | Co |
| 2020 | Development of artificial neural network system to recommend process conditions of injection molding for various geometries | *Advanced Intelligent Systems* | **First** |

**Funded projects**
- LS mtron (2018–2019) — AI injection-molding system, 60%+ mold set-up time reduction.
- POSCO (2020–2021) — Coil temperature deviation minimization in three-row curving yard.
- KITECH (2020–2025) — Intelligent root technology with add-on modules.

---

## Pillar 2 — Nanophotonics Optimization (나노포토닉스 최적화)

> Inverse design of metasurfaces and metamaterials using adjoint methods,
> automatic differentiation, neural surrogates, and global optimizers (PSO, GA, CMA-ES, DDQN, GP).
> *Industry partners: LG Display, Samsung Display, Hanwha Defense, Korea University.*

**Core publications**

| Year | Title | Venue | Role |
|------|-------|-------|------|
| 2025 | Benchmarking Optimization Methods Enabling Efficient Designs for Diverse Nanophotonic Applications | *Advanced Optical Materials* | **First** |
| 2025 | Structurally reordered crystalline atomic layer-dielectric hybrid metasurfaces for near-unity efficiency in the visible | *Materials Today* | Co |
| 2024 | Inverse-designed metasurface for highly saturated transmissive colors | *JOSA B* | Co-first |
| 2024 | Neutral-Colored Transparent Radiative Cooler by Tailoring Solar Absorption with Punctured Bragg Reflectors | *Advanced Functional Materials* | Co |
| 2023 | Inverse design meets nanophotonics: From computational optimization to artificial neural network | *Intelligent Nanotechnology* | Co-first (review) |
| 2022 | Concurrent Optimization of Diffraction Fields from Binary Phase Mask for 3D Nanopatterning | *ACS Photonics* | **First** |
| 2022 | Tutorial on metalenses for advanced flat optics | *J. Applied Physics* | Co-first (62 citations) |
| 2022 | Multicolor and 3D holography realized by inverse design of single-celled metasurfaces | *Advanced Materials* | Co (**271 citations**) |
| 2020 | Scalable and high-throughput top-down manufacturing of optical metasurfaces | *Sensors* | Co-first (60 citations) |

**Funded projects**
- LG Display (2020–2021) — Metasurface light control for OLED.
- LG Display (2021–2022) — Ultra-high-resolution metasurface color filter.
- Samsung Display (2022–2024) — High-refractive polymer absorber metalens.
- Hanwha Defense (2020–2021) — X-band metasurface propagation transformation.
- Korea University (2022–2025) — Hologram Printing & Encoding of Super-Depth-3D Pattern (HOPE).

---

## Pillar 3 — Materials Optimization (소재 최적화)

> AI-driven materials design and property prediction, grounded in constitutive
> relations and microstructure–property mappings.

**Core publications**

| Year | Title | Venue | Role |
|------|-------|-------|------|
| 2025 | Multi-fidelity learning-based latent diffusion model for 3D inverse microstructure design of dual phase steels | *Materials & Design* | Co |
| 2023 | Rheological Behavior of Water-atomized 316L Stainless Steel Powder depending on Particle Size | *Metals and Materials International* | Co |
| 2019 | Analysis of cold compaction for Fe-C, Fe-C-Cu powder design based on constitutive relation and ANN | *Powder Technology* | Co-first |
| 2019 | Correlation Study Between Material Parameters and Mechanical Properties of Iron–Carbon Compacts | *Metals and Materials International* | Co |

---

## Pillar 4 — Metal Autonomous Laboratory (금속 자율실험실)

> Closing the loop between simulation, optimization, and physical experiment
> for metal alloys. Active learning + Bayesian optimization driving efficient discovery.
> *International collaboration: Leibniz IFW Dresden (Prof. Konrad Kosiba).*

**Core publication**

| Year | Title | Venue | Role |
|------|-------|-------|------|
| 2021 | Optimizing laser powder bed fusion of Ti-5Al-5V-5Mo-3Cr by artificial intelligence | *J. Alloys and Compounds* | Co-first (62 citations) |

This pillar is the next phase of the work — translating the optimization toolkit into closed-loop experimentation hardware at KIMS.

---

## Publication Trajectory

```mermaid
xychart-beta
    title "Peer-Reviewed Publications per Year"
    x-axis [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
    y-axis "Publications" 0 --> 6
    bar [2, 2, 2, 3, 4, 5, 4, 1]
```

```mermaid
pie title Publications by Research Pillar
    "Nanophotonics" : 12
    "Materials" : 6
    "Manufacturing" : 3
    "Autonomous Metal Lab" : 2
```

---

## Top-Cited Papers

| Citations | Title | Venue | Year |
|-----------|-------|-------|------|
| 271 | Multicolor and 3D holography by inverse design of single-celled metasurfaces | *Adv. Materials* | 2022 |
| 62 | Tutorial on metalenses for advanced flat optics | *J. Appl. Phys.* | 2022 |
| 62 | Optimizing laser powder bed fusion of Ti-5Al-5V-5Mo-3Cr by AI | *J. Alloys Compd.* | 2021 |
| 60 | Scalable and high-throughput top-down manufacturing of optical metasurfaces | *Sensors* | 2020 |
| 59 | Design of a transmissive metasurface antenna using deep neural networks | *Opt. Mater. Express* | 2021 |

---

## Patents

```mermaid
flowchart LR
    P1["3D Proximity-Field<br/>Nanopatterning Mask<br/>2023 · Korea"]:::active
    P2["Meta-Optical Device<br/>2023 · Samsung Display"]:::active
    P3["AI-Based Hot-Rolled<br/>Coil Placement<br/>2023 · POSCO"]:::active
    P4["AI-Based Injection<br/>Molding System<br/>2021 · PCT"]:::pct
    P5["Bicycle ABS<br/>2017 · Korea"]:::active
    classDef active fill:#FAF7F0,stroke:#CC785C,stroke-width:1.5px,color:#2A2A2A
    classDef pct fill:#FAF7F0,stroke:#7A8C7E,stroke-width:1.5px,color:#2A2A2A
```

| # | Title (EN) | Number | Year |
|---|-----------|--------|------|
| 1 | Electric-field-controlled 3D proximity-field patterning mask | 10-2023-0135822 | 2023 |
| 2 | Meta-optical device manufacturing (Samsung Display) | 10-2023-0085299 | 2023 |
| 3 | AI-based hot-rolled coil placement system (POSCO) | 10-2023-0133116 | 2023 |
| 4 | AI-based injection molding system | **WO 2021/049848 A1** (PCT) | 2021 |
| 5 | ABS for bicycles | 10-2017-0027222 | 2017 |

---

## Conference Talks

**International (7)** — Metamaterials 2024 (Crete, oral), Nano Korea 2023 (oral), MRS Spring 2023 (San Francisco, poster), Nano Convergence 2021 (virtual poster), IIMC 2019 (Aachen, oral), PM World Congress 2018 (Beijing, oral), AISM 2017 (Pohang, oral).

**Domestic (4)** — KSME Micro/Nano 2022 (oral), KSME Micro/Nano 2020 (poster), KSDME Winter 2018 (oral), KPMI 2018 (oral).

---

## Collaboration Network

```mermaid
flowchart LR
    Lee(("Chihun Lee<br/>KIMS")):::center

    subgraph Industry [Industrial Partners]
        direction TB
        POSCO[POSCO<br/>hot-rolled coil]
        Samsung[Samsung Display<br/>metalens]
        LG[LG Display<br/>metasurface color filter / OLED]
        Hanwha[Hanwha Defense<br/>X-band metasurface]
        LSm[LS mtron<br/>injection molding]
        KITECH[KITECH<br/>intelligent root]
    end

    subgraph Academic [Academic Collaborators]
        direction TB
        Rho[Prof. Junsuk Rho<br/>POSTECH · Ph.D. advisor]
        SPark[Prof. Seongjin Park<br/>POSTECH · M.S. advisor]
        Jeon[Prof. Seokwoo Jeon<br/>Korea U · 3D nanopatterning]
        Kosiba[Prof. Konrad Kosiba<br/>Leibniz IFW Dresden · LPBF]
        Bibow[Dr. Pascal Bibow<br/>IKV-AACHEN · injection molding]
        Chung[Prof. Haejun Chung<br/>Hanyang U · adjoint metalens]
    end

    Lee --- POSCO & Samsung & LG & Hanwha & LSm & KITECH
    Lee --- Rho & SPark & Jeon & Kosiba & Bibow & Chung

    classDef center fill:#CC785C,stroke:#B85A3C,stroke-width:2px,color:#FFFFFF
```

---

## Career Timeline

```mermaid
timeline
    title Career & Education
    2013–2018 : B.S. Mechanical Engineering, POSTECH
    2018–2019 : M.S. Mechanical Engineering, POSTECH : Advisor — Prof. Seongjin Park
    2018      : Guest Researcher, KITECH : PI — Dr. Dongyoung Park
    2020–2025 : Ph.D. Mechanical Engineering, POSTECH : Advisor — Prof. Junsuk Rho
    2022–2025 : Technical Research Personnel (Alternative Military Service)
    2025–now  : Senior Researcher, KIMS : Material Data & Analysis Research Division
```

---

## Technical Stack

**Forward simulation** — RCWA (in-house MATLAB) · FDTD (Lumerical, MEEP) · FEM (COMSOL) · Bulk optics (VirtualLab Fusion) · Scalar diffraction (in-house MATLAB).

**Learning & optimization** — PyTorch · TensorFlow · PSO · GA · CMA-ES · Adjoint method · Automatic differentiation · DDQN · Simulated Annealing · Gaussian Process (Bayesian Optimization).

**Manufacturing apps** — Injection molding · Hot-rolled coil placement · Punch press · Drilling · DED metal 3D printing · Powder injection molding · Powder manufacturing.

**Nanophotonics apps** — LED simulation & collimation · 3D patterning mask design · Color filter · Nano antenna · Achromatic metalens · Meta-hologram · Beam forming.

---

## What's Next

1. **Closing the autonomous metal lab loop** — Translate the LPBF optimization framework into an on-instrument active-learning controller at KIMS.
2. **Microstructure inverse design** — Extend the multi-fidelity latent diffusion approach (Jung et al. 2025) toward goal-conditioned generation for dual-phase and high-entropy alloys.
3. **Cross-pillar transfer** — Apply nanophotonic optimization tooling (adjoint, AD, neural surrogates) to manufacturing process design where gradients can be defined through differentiable simulators.

---

*This file is human-curated. The underlying facts live in `data/*.yaml` — edit there and run `./rebuild_all.sh` to propagate to CV, website, and LinkedIn drafts.*
