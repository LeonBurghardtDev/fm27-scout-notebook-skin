import re, sys
skin = sys.argv[1]
src = open(f"{skin}/theme.uss", encoding="utf-8").read()

C = {  # base RGB used for alpha companions
 "surface-canvas": (27,25,21), "surface-page": (33,30,26), "surface-panel": (42,39,35),
 "brand-primary": (183,160,110), "brand-accent": (183,160,110), "brand-primary-hover": (201,180,132),
 "feedback-danger-surface": (70,38,30), "feedback-danger": (222,128,104), "on-media": (238,231,216),
}
rgb = lambda t: "rgb(%d, %d, %d)" % t
fonts = lambda f: f'url("fonts/{f}.ttf")'

T = {
 # surfaces: dark desk, sheet cards
 "surface-canvas": rgb(C["surface-canvas"]), "surface-page": rgb(C["surface-page"]),
 "surface-navigation": "rgb(27, 25, 21)", "surface-panel": rgb(C["surface-panel"]),
 "surface-raised": "rgb(50, 46, 41)", "surface-strong": "rgb(62, 57, 49)",
 # ink
 "text-primary": "rgb(238, 231, 216)", "text-secondary": "rgb(189, 180, 162)",
 "text-disabled": "rgb(140, 132, 117)", "ink": "#221E17",
 # gold lines
 "border-default": "rgb(91, 81, 61)", "border-subtle": "rgb(73, 66, 51)",
 "control-background": "rgb(50, 46, 41)", "control-hover": "rgb(60, 55, 48)",
 "control-pressed": "rgb(72, 65, 55)", "control-border": "rgb(110, 98, 74)",
 "selection-muted": "rgb(58, 52, 42)",
 # brand = notebook gold
 "focus-ring": "rgb(217, 196, 143)", "brand-primary": rgb(C["brand-primary"]),
 "brand-primary-hover": rgb(C["brand-primary-hover"]), "brand-primary-pressed": "rgb(150, 129, 84)",
 "brand-on-primary": "rgb(34, 30, 23)", "brand-accent-soft": "rgb(217, 196, 143)",
 # notebook cards: hairline gold frame, square
 "card-border-width": "1px", "card-border-colour": "var(--skin-border-subtle)",
 "dialog-border": "var(--skin-brand-primary)",
 "nav-active-indicator": "var(--skin-brand-primary)",
 "table-row-alternate-background": "rgba(183, 160, 110, 0.06)",
 "list-selection-background": "rgb(62, 55, 42)",
 # warm data palette
 "data-sky": "rgb(143, 180, 190)", "data-amber": "rgb(232, 185, 106)",
 "data-mint": "rgb(162, 190, 134)", "data-coral": "rgb(214, 130, 106)",
 "data-blue": "rgb(140, 160, 196)", "data-sand": "rgb(217, 196, 143)",
 "data-steel": "rgb(160, 170, 165)", "data-rose": "rgb(200, 150, 140)",
 "data-comparison-cyan": "rgb(143, 196, 184)", "data-comparison-orange": "rgb(232, 165, 80)",
 "finance-category-fund-raising-colour": "#A89F8C", "finance-category-other-colour": "#EEE7D8",
 # feedback
 "feedback-warning": "rgb(232, 185, 106)", "feedback-warning-surface": "rgb(66, 52, 32)",
 "feedback-danger": rgb(C["feedback-danger"]), "feedback-danger-surface": rgb(C["feedback-danger-surface"]),
 "feedback-success": "rgb(162, 200, 128)", "feedback-success-surface": "rgb(40, 52, 32)",
 "feedback-info": "rgb(150, 180, 200)", "feedback-info-surface": "rgb(34, 46, 54)",
 "medical-risk-high-background": "rgb(64, 40, 30)", "medical-risk-high-foreground": "rgb(232, 150, 106)",
 "on-media": rgb(C["on-media"]),
 # type: IBM Plex Sans throughout (mono nav was too wide and truncated tabs)
 "font-family-primary": fonts("IBMPlexSans-Regular"),
 "font-family-display": fonts("IBMPlexSans-SemiBold"),
 "font-family-navigation": fonts("IBMPlexSans-SemiBold"),
 "font-secondary-navigation": fonts("IBMPlexSans-Regular"),
 # Plex sets larger than Poppins at the same size: step the text range down by 1-2px
 "font-size-13": "12px", "font-size-14": "13px", "font-size-15": "14px", "font-size-16": "15px",
 "font-size-18": "16px", "font-size-19": "17px", "font-size-20": "18px", "font-size-22": "20px",
 "font-size-24": "22px", "font-size-26": "24px", "font-size-30": "27px",
 "font-secondary-navigation-size": "var(--skin-font-size-13)",
 "menu-tile-heading-size": "var(--heading-md-size)",
 "font-family-condensed": fonts("IBMPlexSansCondensed-Regular"),
 # square corners (pill stays round so toggles still read as toggles)
 "radius-micro": "0px", "radius-hairline": "0px", "radius-compact": "0px", "radius-small": "0px",
 "radius-medium": "0px", "radius-control": "0px", "radius-tight": "0px", "radius-card": "0px",
 "radius-shell": "0px", "radius-extra-large": "0px",
}
# data alpha-16 companions
for k in ["data-sky","data-amber","data-mint","data-coral","data-comparison-cyan","data-comparison-orange"]:
    r = tuple(map(int, re.findall(r"\d+", T[k])))
    T[k+"-alpha-16"] = "rgba(%d, %d, %d, 0.16)" % r

# regenerate every alpha companion defined in the template
names = sorted(C, key=len, reverse=True)
for m in re.finditer(r"--skin-([a-z0-9-]+)-alpha-(\d+):\s*rgba\([^)]*\)", src):
    base, a = m.group(1), m.group(2)
    if base in C:
        T[f"{base}-alpha-{a}"] = "rgba(%d, %d, %d, %s)" % (*C[base], f"{int(a)/100:g}")
    else:
        print("unmapped alpha:", base, a)

defined = set(re.findall(r"--skin-([a-z0-9-]+):", src))
missing = [k for k in T if k not in defined]
if missing: print("NOT IN TEMPLATE:", missing)

out = ["/* Scout Notizbuch — token overrides on top of theme.uss.",
       " * Palette: dark sheet, cream ink, gold lines. IBM Plex type.",
       " * Change a colour here; keep its -alpha-* companions in sync (gen script). */",
       ":root {"]
out += [f"  --skin-{k}: {v};" for k, v in T.items()]
out.append("}\n")
open(f"{skin}/theme-scout.uss", "w", encoding="utf-8", newline="\n").write("\n".join(out))
print(len(T), "tokens written")
