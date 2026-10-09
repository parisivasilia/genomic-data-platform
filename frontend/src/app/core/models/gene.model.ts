export interface GeneSummary {
  id: string;
  symbol: string | null;
  description: string | null;
  geneType: string | null;
  chromosome: string | null;
  startPosition: number | null;
  endPosition: number | null;
  strand: number | null;
  gcContent: number | null;
}

export interface GeneDetail extends GeneSummary {
  synonyms: string[];
  sourceName: string;
  sourceVersion: string;
  referenceAssembly: string;
  sourceUrl: string | null;
}

export interface Transcript {
  id: string;
  name: string | null;
  transcriptType: string | null;
  chromosome: string | null;
  startPosition: number | null;
  endPosition: number | null;
  strand: number | null;
  geneId: string;
  sourceName: string;
  sourceVersion: string;
  referenceAssembly: string;
}

export interface Variant {
  clinvarVariationId: number;
  clinvarAccession: string | null;
  rsId: string | null;
  chromosome: string | null;
  position: number | null;
  referenceAllele: string | null;
  alternateAllele: string | null;
  variantType: string | null;
  classificationType: string | null;
  clinicalSignificance: string | null;
  reviewStatus: string | null;
  lastEvaluated: string | null;
  sourceName: string;
  sourceVersion: string;
  referenceAssembly: string;
}

export interface CuratedAnnotation {
  id: number;
  geneId: string;
  title: string;
  annotationText: string;
  category: string | null;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
}

export interface CuratedAnnotationRequest {
  title: string;
  annotationText: string;
  category: string | null;
}

export interface LoginResponse {
  accessToken: string;
  tokenType: string;
  expiresIn: number;
}

export interface PageResponse<T> {
  content: T[];
  number: number;
  size: number;
  totalElements: number;
  totalPages: number;
  numberOfElements: number;
  first: boolean;
  last: boolean;
  empty: boolean;
}
