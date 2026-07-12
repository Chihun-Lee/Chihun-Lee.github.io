# SYNC — 연구 정체성 한 번에 업데이트

`data/*.yaml`(SSOT)을 고치면 아래 4개 채널을 한 번에 최신화한다.
목표: **YAML 한 곳만 수정 → CV·웹사이트·LinkedIn·Scholar 대조까지 일괄.**

| 채널 | 자동화 | 명령/방법 |
|---|---|---|
| CV (Typst PDF) | ✅ 완전자동 | `./rebuild_all.sh cv` |
| Website (Astro, chihun-lee.github.io) | ✅ 완전자동 | `./rebuild_all.sh site` → `git push` (GH Action 배포) |
| LinkedIn **게시물 초안** | ✅ 자동(초안만) | `./rebuild_all.sh sns` → `SNS/posts/*.md` 복붙 |
| LinkedIn **프로필**(경력·학력·논문·스킬) | ⚠️ 반자동 | Claude-in-Chrome, 아래 절차 |
| Google Scholar 대조 | ⚠️ 수동확인 | 아래 절차 |

전체 재빌드: `./rebuild_all.sh` (CV + LinkedIn 초안 + Website)

---

## 1. Google Scholar 대조 (새 논문 유입 확인)

1. https://scholar.google.com/citations?user=Na1nYPsAAAAJ&pagesize=100 열기
2. `data/publications.yaml`과 제목 대조 → 누락분 추가.
   - ⚠️ 동명이인 오검출 1건 주의: **"Ageing and rejuvenation ... microbial communities" (Microbiome)** 는 본인 논문 아님. 제외.
3. `scholar_metrics`(citations·h-index·i10) 갱신, `last_updated` 수정.
4. 추가 후 `./rebuild_all.sh` 로 CV·웹사이트 반영.

## 2. LinkedIn 프로필 동기화 (Claude-in-Chrome)

**계정/URL 고정값 (2026-07 기준)**
- 표시 이름: **Chihun Lee** (영문). 프로필 2언어: Korean(기본)+English.
- URL: **https://www.linkedin.com/in/chihun-lee-078082412/**
  - 짧은 `chihun-lee`는 **동명이인(덴마크 Microsoft 엔지니어)이 선점** → 사용 불가, 항상 `-078082412` 붙일 것.
  - `/in/me/` 로 자기 프로필 실제 슬러그 확인 가능.

**편집 자동화 팁 (검증됨)**
- 로그인된 로컬 Chrome + Claude-in-Chrome 필요.
- 폼 입력은 `form_input`(ref), **저장 버튼은 a11y 트리에 안 잡히므로** JS로 클릭:
  `[...document.querySelectorAll('button')].filter(x=>x.textContent.trim()==='저장'&&x.offsetParent).pop().click()`
- **날짜 필드 형식은 `YYYY. M. D`** (예: `2025. 11. 12`). `YYYY-MM-DD`는 거부됨.
- 논문 개별 편집 URL: `/in/chihun-lee-078082412/details/publications/edit/forms/{id}/`
  (id는 상세 페이지 `a[href*="/edit/forms/"]`에서 추출. 리스트가 가상화되어 10개씩만 렌더 → 새 탭+대기 필요. 종종 로딩 지연/스로틀 발생.)
- 경력·학력은 국문 저장 후 English 탭에서 영문 별도 입력.

**현재 프로필 구성 (동기화 완료분)**
- 경력 5: UST 조교수(2026.9~) · KIMS 선임연구원(2025.2~) · POSTECH 전문연구요원 · KITECH 객원연구원
- 학력 3: POSTECH 박사·석사·학사
- 논문 24편 등록 완료
- 스킬 5: 인공지능(AI) · 머신러닝 · Nanophotonics · Self-driving laboratory · AI for Manufacturing

## 3. 논문 발행일 (정확한 값 — Scholar/Crossref 검증, 2026-07)

LinkedIn·CV·웹사이트 모두 이 날짜를 쓸 것. 대부분 "online 최초공개일".

| 논문(약칭) | 게재지 | 발행일 |
|---|---|---|
| Parameter-aware ... stable diffusion | Adv. Eng. Informatics | 2025-11-12 |
| Benchmarking Optimization Methods | Adv. Optical Materials | 2025-05-05 |
| Structurally reordered ... hybrid metasurfaces | Materials Today | 2025-06-13 |
| Real-Time Hot-Rolled Coil ... | Adv. Intelligent Systems | 2025-05-06 |
| Multi-fidelity latent diffusion (dual phase) | Materials & Design | 2025-08-20 |
| Neutral-Colored Transparent Radiative Cooler | Adv. Functional Materials | 2024-08-12 |
| Inverse-designed metasurface (transmissive colors) | JOSA B | 2023-12-08 |
| Inverse design of colored daytime coolers | Sol. Energy Mater. Sol. Cells | 2024-04-05 |
| ANN-Based Process Recommender (Additive Mfg) | EECSS'23 proc. | 2023-08-01 |
| Quantitative Correlation Brazed SUS304/MBF60 | SSRN preprint | 2024-03-22 |
| Utilizing DNN ... Multilayered Coolers | MRS Proceedings | 2023 (월 미확인) |
| Rheological ... 316L SS Powder | Metals and Materials Int'l | 2023-04-15 |
| Inverse design meets nanophotonics | Intelligent Nanotechnology | 2023-01-27 |
| Multicolor and 3D holography (single-cell) | Advanced Materials | 2023-03-18 |
| Concurrent Optimization ... Binary Phase Mask | ACS Photonics | 2022-10-13 |
| Design of transmissive metasurface antenna | Optical Materials Express | 2021-06-24 |
| Correlation Study ... Iron-Carbon Compacts | Metals and Materials Int'l | 2019-05-08 |
| Tutorial on metalenses | J. Applied Physics | 2022-03-04 |
| Mass production superhydrophilic Cu | Powder Technology | 2022-07-30 |
| Optimizing LPBF Ti-5Al-5V-5Mo-3Cr | J. Alloys and Compounds | 2021-05-15 (issue) |
| Development of ANN ... injection molding | Adv. Intelligent Systems | 2020-07-23 |
| Scalable ... top-down metasurfaces | Sensors | 2020-07-23 |
| Analysis of cold compaction Fe-C(-Cu) | Powder Technology | 2019-05-20 |
| Compressing the Validation Bottleneck | ICML 2026 AI4Science WS | 2026-07-10 |

### LinkedIn 논문 날짜 수정 진행상태 (2026-07-12)
- ✅ 완료(10): Parameter-aware, Benchmarking, Structurally, Real-Time, Multi-fidelity, Neutral-Colored, Inverse-designed metasurface, Inverse colored coolers, ANN Process Recommender, Compressing.
- ⏳ 미완(13, 아직 1월1일): Quantitative SUS304, Rheological 316L, Inverse-meets-nanophotonics, Multicolor holography, Concurrent Binary Phase, Transmissive antenna, Iron-Carbon Correlation, Tutorial metalenses, Superhydrophilic Cu, LPBF Ti, ANN injection, Scalable metasurfaces, Cold compaction.
  (상세 페이지 리스트 가상화/로딩 스로틀로 나머지 편집 ID 확보 실패 → 세션 재개 시 이어서.)
