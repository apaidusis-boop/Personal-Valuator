/**
 * SectionHeader.tsx — mirror of scripts/_components.py::section_header.
 *
 * Caption ≤ 8 palavras (DS008). Se mais, refactor para parágrafo.
 */
export function SectionHeader({ title, caption }: { title: string; caption?: string }) {
  return (
    <div className="section-header">
      <div className="section-header__title">{title}</div>
      {caption && <div className="section-header__caption">{caption}</div>}
    </div>
  );
}
