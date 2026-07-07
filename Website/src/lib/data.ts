// Build-time YAML loader: reads SSOT YAML from ../../data/*.yaml.
// All data flows in one direction: YAML -> this module -> Astro pages.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import yaml from 'js-yaml';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_DIR = path.resolve(__dirname, '../../../data');

function load<T>(file: string): T {
  const p = path.join(DATA_DIR, file);
  const raw = fs.readFileSync(p, 'utf8');
  // JSON_SCHEMA: keep ISO dates (e.g. 2026-07-07) as plain strings, not Date objects.
  return yaml.load(raw, { schema: yaml.JSON_SCHEMA }) as T;
}

// ── Types ────────────────────────────────────────────────────────────
export type PillarId =
  | 'manufacturing'
  | 'nanophotonics'
  | 'materials'
  | 'autonomous-metal-lab';

export interface Pillar {
  id: PillarId;
  title: string;
  kr: string;
  color: string;
  blurb: string;
}

export interface Profile {
  name: string;
  name_kr: string;
  honorific: string;
  title: string;
  affiliation: string;
  affiliation_kr: string;
  division: string;
  nationality: string;
  contact: {
    email: string;
    office_phone: string;
    mobile: string;
    location: string;
  };
  links: {
    scholar: string;
    github: string;
    orcid?: string;
    linkedin?: string;
    website: string;
  };
  scholar_metrics: {
    total_citations: number;
    h_index: number;
    i10_index: number;
    last_updated: string;
  };
  short_bio: string;
  long_bio: string;
  research_interests: string[];
  research_pillars: Pillar[];
  education: Array<Record<string, any>>;
  experience: Array<Record<string, any>>;
  specializations: Record<string, string[]>;
  collaborations: Array<Record<string, any>>;
}

export interface Publication {
  id: string;
  title: string;
  authors: string[];
  venue: string;
  volume?: string;
  issue?: string;
  pages?: string;
  year: number;
  role: 'first' | 'co_first' | 'co' | 'corresponding';
  pillar: PillarId;
  equal_contribution?: boolean;
  type?: string;
  industry_partner?: string;
  doi?: string;
  url?: string;
  citations?: number;
}

export interface Project {
  title: string;
  sponsor: string;
  role: string;
  start: string;
  end: string;
  pillar: PillarId;
}

export interface Talk {
  title: string;
  authors: string[];
  venue: string;
  location: string;
  date: string;
  role: 'oral' | 'poster' | 'virtual_poster' | 'invited' | 'keynote';
  type: 'international' | 'domestic';
}

export interface NewsItem {
  date: string;
  text: string;
}

export interface Person {
  name: string;
  name_kr?: string;
  role?: string;
  institution: string;
  period?: string;
  lab?: string;
  topic?: string;
  website?: string;
  photo?: string;
  bio?: string;
}

export interface Patent {
  title: string;
  title_en: string;
  inventors: string[];
  number: string;
  jurisdiction: string;
  assignee?: string;
  year: number;
}

// ── Loaders ──────────────────────────────────────────────────────────
export const profile: Profile = load<Profile>('profile.yaml');
export const publications: Publication[] =
  load<{ publications: Publication[] }>('publications.yaml').publications;
export const projects: Project[] =
  load<{ projects: Project[] }>('projects.yaml').projects;
const talksFile = load<{ talks: Talk[]; travel: any[] }>('talks.yaml');
export const talks: Talk[] = talksFile.talks;
export const travel = talksFile.travel;
export const news: NewsItem[] = load<{ news: NewsItem[] }>('news.yaml').news;
const peopleFile = load<{
  lead: Person;
  advisors: Person[];
  collaborators: Person[];
  students: Person[];
}>('people.yaml');
export const lead = peopleFile.lead;
export const advisors = peopleFile.advisors;
export const collaborators = peopleFile.collaborators;
export const students = peopleFile.students;
export const patents: Patent[] =
  load<{ patents: Patent[] }>('patents.yaml').patents;

// ── Helpers ──────────────────────────────────────────────────────────
export function formatAuthors(authors: string[]): string {
  // Strip trailing markers (+, *) for display, but flag "C. Lee" / "Chihun Lee"
  return authors
    .map((a) => a.replace(/[+*]+$/, '').trim())
    .join(', ');
}

export function isMe(author: string): boolean {
  const a = author.replace(/[+*]+$/, '').trim().toLowerCase();
  return a === 'c. lee' || a === 'chihun lee' || a === 'c.lee';
}

export function publicationsByYear(pubs: Publication[]) {
  const byYear = new Map<number, Publication[]>();
  for (const p of pubs) {
    if (!byYear.has(p.year)) byYear.set(p.year, []);
    byYear.get(p.year)!.push(p);
  }
  return [...byYear.entries()].sort((a, b) => b[0] - a[0]);
}

export function pubsForPillar(pillar: PillarId): Publication[] {
  return publications.filter((p) => p.pillar === pillar);
}
export function projectsForPillar(pillar: PillarId): Project[] {
  return projects.filter((p) => p.pillar === pillar);
}
