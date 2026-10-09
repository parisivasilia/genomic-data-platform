import {
  HttpClient,
  HttpHeaders,
  HttpParams,
} from '@angular/common/http';
import {
  inject,
  Injectable,
} from '@angular/core';
import { Observable } from 'rxjs';

import { AuthService } from '../auth/auth.service';
import {
  CuratedAnnotation,
  CuratedAnnotationRequest,
  GeneDetail,
  GeneSummary,
  PageResponse,
  Transcript,
  Variant,
} from '../models/gene.model';

export interface GeneSearchFilters {
  symbol?: string;
  chromosome?: string;
  geneType?: string;
  keyword?: string;
  page?: number;
  size?: number;
}

@Injectable({
  providedIn: 'root',
})
export class GenomicApiService {
  private readonly http = inject(HttpClient);
  private readonly auth = inject(AuthService);

  getGenes(
    filters: GeneSearchFilters = {},
  ): Observable<PageResponse<GeneSummary>> {
    let params = new HttpParams()
      .set('page', filters.page ?? 0)
      .set('size', filters.size ?? 20);

    if (filters.symbol?.trim()) {
      params = params.set(
        'symbol',
        filters.symbol.trim(),
      );
    }

    if (filters.chromosome?.trim()) {
      params = params.set(
        'chromosome',
        filters.chromosome.trim(),
      );
    }

    if (filters.geneType?.trim()) {
      params = params.set(
        'geneType',
        filters.geneType.trim(),
      );
    }

    if (filters.keyword?.trim()) {
      params = params.set(
        'keyword',
        filters.keyword.trim(),
      );
    }

    return this.http.get<PageResponse<GeneSummary>>(
      '/api/v1/genes',
      { params },
    );
  }

  getGene(
    geneId: string,
  ): Observable<GeneDetail> {
    return this.http.get<GeneDetail>(
      `/api/v1/genes/${geneId}`,
    );
  }

  getTranscripts(
    geneId: string,
  ): Observable<PageResponse<Transcript>> {
    return this.http.get<PageResponse<Transcript>>(
      `/api/v1/genes/${geneId}/transcripts`,
      {
        params: new HttpParams().set(
          'size',
          100,
        ),
      },
    );
  }

  getVariants(
    geneId: string,
  ): Observable<PageResponse<Variant>> {
    return this.http.get<PageResponse<Variant>>(
      `/api/v1/genes/${geneId}/variants`,
      {
        params: new HttpParams().set(
          'size',
          100,
        ),
      },
    );
  }

  getAnnotations(
    geneId: string,
  ): Observable<CuratedAnnotation[]> {
    return this.http.get<CuratedAnnotation[]>(
      `/api/v1/genes/${geneId}/annotations`,
    );
  }

  createAnnotation(
    geneId: string,
    request: CuratedAnnotationRequest,
  ): Observable<CuratedAnnotation> {
    return this.http.post<CuratedAnnotation>(
      `/api/v1/admin/genes/${geneId}/annotations`,
      request,
      {
        headers: this.adminHeaders(),
      },
    );
  }

  updateAnnotation(
    id: number,
    request: CuratedAnnotationRequest,
  ): Observable<CuratedAnnotation> {
    return this.http.put<CuratedAnnotation>(
      `/api/v1/admin/annotations/${id}`,
      request,
      {
        headers: this.adminHeaders(),
      },
    );
  }

  deleteAnnotation(
    id: number,
  ): Observable<void> {
    return this.http.delete<void>(
      `/api/v1/admin/annotations/${id}`,
      {
        headers: this.adminHeaders(),
      },
    );
  }

  private adminHeaders(): HttpHeaders {
    const token = this.auth.getToken();

    if (!token) {
      return new HttpHeaders();
    }

    return new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });
  }
}
