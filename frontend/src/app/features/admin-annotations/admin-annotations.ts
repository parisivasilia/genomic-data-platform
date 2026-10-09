import {
  Component,
  inject,
  signal,
} from '@angular/core';
import { DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

import { AuthService } from '../../core/auth/auth.service';
import {
  CuratedAnnotation,
  CuratedAnnotationRequest,
} from '../../core/models/gene.model';
import { GenomicApiService } from '../../core/services/genomic-api.service';

@Component({
  selector: 'app-admin-annotations',
  imports: [
    DatePipe,
    FormsModule,
    RouterLink,
  ],
  templateUrl: './admin-annotations.html',
  styleUrl: './admin-annotations.scss',
})
export class AdminAnnotationsPage {
  private readonly api =
    inject(GenomicApiService);

  private readonly auth =
    inject(AuthService);

  readonly annotations =
    signal<CuratedAnnotation[]>([]);

  readonly loadedGeneId = signal('');
  readonly loading = signal(false);
  readonly working = signal(false);
  readonly error = signal('');
  readonly message = signal('');

  geneId = '';
  title = '';
  annotationText = '';
  category = '';

  editingId: number | null = null;

  loadAnnotations(): void {
    const geneId = this.geneId.trim();

    if (!geneId) {
      this.error.set(
        'Enter an Ensembl gene ID.',
      );
      return;
    }

    this.loading.set(true);
    this.error.set('');
    this.message.set('');

    this.api
      .getAnnotations(geneId)
      .subscribe({
        next: (annotations) => {
          this.annotations.set(
            annotations,
          );

          this.loadedGeneId.set(
            geneId,
          );

          this.loading.set(false);

          if (annotations.length === 0) {
            this.message.set(
              `No curated annotations found for ${geneId}.`,
            );
          } else {
            const label =
              annotations.length === 1
                ? 'annotation'
                : 'annotations';

            this.message.set(
              `Loaded ${annotations.length} curated ${label} for ${geneId}.`,
            );
          }
        },
        error: () => {
          this.annotations.set([]);
          this.loadedGeneId.set('');
          this.loading.set(false);

          this.error.set(
            'Unable to load annotations. Check the gene ID.',
          );
        },
      });
  }

  saveAnnotation(): void {
    const geneId = this.geneId.trim();
    const title = this.title.trim();
    const annotationText =
      this.annotationText.trim();

    if (
      !geneId ||
      !title ||
      !annotationText
    ) {
      this.error.set(
        'Gene ID, title, and annotation text are required.',
      );
      return;
    }

    const request: CuratedAnnotationRequest = {
      title,
      annotationText,
      category:
        this.category.trim() || null,
    };

    this.working.set(true);
    this.error.set('');
    this.message.set('');

    const operation =
      this.editingId === null
        ? this.api.createAnnotation(
            geneId,
            request,
          )
        : this.api.updateAnnotation(
            this.editingId,
            request,
          );

    operation.subscribe({
      next: () => {
        const wasEditing =
          this.editingId !== null;

        this.clearForm();
        this.working.set(false);

        this.message.set(
          wasEditing
            ? 'Annotation updated.'
            : 'Annotation created.',
        );

        this.reloadCurrentGene();
      },
      error: () => {
        this.working.set(false);

        this.error.set(
          'The protected operation failed. Your session may have expired.',
        );
      },
    });
  }

  edit(
    annotation: CuratedAnnotation,
  ): void {
    this.editingId = annotation.id;
    this.geneId = annotation.geneId;
    this.title = annotation.title;
    this.annotationText =
      annotation.annotationText;
    this.category =
      annotation.category ?? '';

    this.error.set('');
    this.message.set('');
  }

  cancelEdit(): void {
    this.clearForm();
  }

  deleteAnnotation(
    annotation: CuratedAnnotation,
  ): void {
    const confirmed = confirm(
      `Delete "${annotation.title}"?`,
    );

    if (!confirmed) {
      return;
    }

    this.working.set(true);
    this.error.set('');
    this.message.set('');

    this.api
      .deleteAnnotation(annotation.id)
      .subscribe({
        next: () => {
          this.working.set(false);

          this.message.set(
            'Annotation deleted.',
          );

          if (
            this.editingId ===
            annotation.id
          ) {
            this.clearForm();
          }

          this.reloadCurrentGene();
        },
        error: () => {
          this.working.set(false);

          this.error.set(
            'Unable to delete the annotation.',
          );
        },
      });
  }

  logout(): void {
    this.auth.logout();
  }

  private reloadCurrentGene(): void {
    const geneId = this.geneId.trim();

    if (!geneId) {
      this.annotations.set([]);
      this.loadedGeneId.set('');
      return;
    }

    this.api
      .getAnnotations(geneId)
      .subscribe({
        next: (annotations) => {
          this.annotations.set(
            annotations,
          );

          this.loadedGeneId.set(
            geneId,
          );
        },
        error: () => {
          this.annotations.set([]);
          this.loadedGeneId.set('');
        },
      });
  }

  private clearForm(): void {
    this.editingId = null;
    this.title = '';
    this.annotationText = '';
    this.category = '';
  }
}
