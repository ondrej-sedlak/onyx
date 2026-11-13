"use client";

import { useTranslations } from "next-intl";
import type { SelectOption } from "@opal/components";
import type { SkillInstallationPolicy } from "@/lib/skills/types";

/** Most open first, as Claude lists them. */
export const INSTALLATION_POLICIES: readonly SkillInstallationPolicy[] = [
  "REQUIRED",
  "DEFAULT",
  "AVAILABLE",
  "NOT_AVAILABLE",
];
/** The one set of level labels and help text. */
export function useInstallationPolicyCopy() {
  const t = useTranslations("skills.installationPolicy");
  return {
    label: (policy: SkillInstallationPolicy) => t(`${policy}.label`),
    description: (policy: SkillInstallationPolicy) =>
      t(`${policy}.description`),
  };
}

interface PolicyOptionsConfig {
  levels?: readonly SkillInstallationPolicy[];
}

/** The select options of an install setting. */
export function usePolicyOptions({
  levels = INSTALLATION_POLICIES,
}: PolicyOptionsConfig = {}): SelectOption[] {
  const copy = useInstallationPolicyCopy();
  const options: SelectOption[] = levels.map((policy) => ({
    value: policy,
    title: copy.label(policy),
    description: copy.description(policy),
  }));
  return options;
}
