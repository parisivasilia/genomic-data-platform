import { DatePipe } from '@angular/common';
import {
  Component,
  inject,
  signal,
} from '@angular/core';
import {
  ActivatedRoute,
  RouterLink,
} from '@angular/router';

import {
  CuratedAnnotation,
  GeneDetail,
  Transcript,
  Variant,
} from '../../core/models/gene.model';
import { GenomicApiService } from '../../core/services/genomic-api.service';

@Component({
  selector: 'app-gene-detail',
  imports: [
    DatePipe,
    RouterLink,
  ],
  templateUrl: './gene-detail.html',
  styleUrl: './gene-detail.scss',
})
export class GeneDetailPage {
  private readonly route =
    inject(ActivatedRoute);

  private readonly api =
    inject(GenomicApiService);

  readonly gene =
    signal<GeneDetail | null>(null);

  readonly transcripts =
    signal<Transcript[]>([]);

  readonly variants =
    signal<Variant[]>([]);

  readonly annotations =
    signal<CuratedAnnotation[]>([]);

  readonly loading = signal(true);
  readonly error = signal('');

  constructor() {
    const geneId =
      this.route.snapshot.paramMap.get('id');

    if (!geneId) {
      this.error.set(
        'Gene ID is missing.',
      );
      this.loading.set(false);
      return;
    }

    this.loadGene(geneId);
    this.loadTranscripts(geneId);
    this.loadVariants(geneId);
    this.loadAnnotations(geneId);
  }

  clinicalSignificanceClass(
    significance:
      | string
      | null
      | undefined,
  ): string {
    const value =
      significance
        ?.toLowerCase()
        .trim()
        .replace(/\s+/g, ' ') ?? '';

    if (
      value.includes('conflicting') ||
      value.includes('conflict')
    ) {
      return 'conflicting';
    }

    if (
      value.includes(
        'uncertain significance',
      ) ||
      value.includes('uncertain') ||
      value.includes('vus')
    ) {
      return 'uncertain';
    }

    if (
      value === 'likely pathogenic'
    ) {
      return 'likely-pathogenic';
    }

    if (
      value.includes('pathogenic')
    ) {
      return 'pathogenic';
    }

    if (value === 'likely benign') {
      return 'likely-benign';
    }

    if (value.includes('benign')) {
      return 'benign';
    }

    return 'other';
  }

  private loadGene(
    geneId: string,
  ): void {
    this.api.getGene(geneId).subscribe({
      next: (gene) => {
        this.gene.set(gene);
        this.loading.set(false);
      },
      error: () => {
        this.error.set(
          'Unable to load gene details.',
        );
        this.loading.set(false);
      },
    });
  }

  private loadTranscripts(
    geneId: string,
  ): void {
    this.api
      .getTranscripts(geneId)
      .subscribe({
        next: (page) => {
          this.transcripts.set(
            page.content,
          );
        },
        error: () => {
          this.transcripts.set([]);
        },
      });
  }

  private loadVariants(
    geneId: string,
  ): void {
    this.api
      .getVariants(geneId)
      .subscribe({
        next: (page) => {
          this.variants.set(
            page.content,
          );
        },
        error: () => {
          this.variants.set([]);
        },
      });
  }

  private loadAnnotations(
    geneId: string,
  ): void {
    this.api
      .getAnnotations(geneId)
      .subscribe({
        next: (annotations) => {
          this.annotations.set(
            annotations,
          );
        },
        error: () => {
          this.annotations.set([]);
        },
      });
  }
}
