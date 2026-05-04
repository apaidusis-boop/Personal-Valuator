import { ReactNode } from "react";

type Props = {
  icon?: ReactNode;
  title: string;
  description?: string;
  action?: ReactNode;
  className?: string;
};

export default function EmptyState({
  icon = "◯",
  title,
  description,
  action,
  className = "",
}: Props) {
  return (
    <div
      className={
        "card p-10 flex flex-col items-center text-center gap-3 " + className
      }
    >
      <div
        className="text-3xl text-[var(--text-tertiary)]"
        aria-hidden
      >
        {icon}
      </div>
      <h3 className="type-h2 text-[var(--text-primary)]">{title}</h3>
      {description && (
        <p className="type-body-sm text-[var(--text-secondary)] max-w-md">
          {description}
        </p>
      )}
      {action}
    </div>
  );
}
