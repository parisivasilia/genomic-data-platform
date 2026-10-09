import {
  Component,
  inject,
  signal,
} from '@angular/core';

import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

import { GeneSummary } from '../../core/models/gene.model';
import { GenomicApiService } from '../../core/services/genomic-api.service';

@Component({
  selector: 'app-gene-explorer',
  imports: [FormsModule, RouterLink],
  templateUrl: './gene-explorer.html',
  styleUrl: './gene-explorer.scss',
})
export class GeneExplorer {
  private readonly api = inject(GenomicApiService);

  readonly genes = signal<GeneSummary[]>([]);
  readonly loading = signal(false);
  readonly error = signal('');
  readonly totalElements = signal(0);

  symbol = '';
  chromosome = '';
  geneType = '';
  keyword = '';

  constructor() {
    this.search();
  }

  search(): void {
    this.loading.set(true);
    this.error.set('');

    this.api.getGenes({
      symbol: this.symbol,
      chromosome: this.chromosome,
      geneType: this.geneType,
      keyword: this.keyword,
      size: 50,
    }).subscribe({
      next: (page) => {
        this.genes.set(page.content);
        this.totalElements.set(page.totalElements,);
        this.loading.set(false);
      },
      error: () => {
        this.error.set(
          'Unable to load genomic data.',
        );
        this.loading.set(false);
      },
    });
  }

  clearFilters(): void {
    this.symbol = '';
    this.chromosome = '';
    this.geneType = '';
    this.keyword = '';

    this.search();
  }
}