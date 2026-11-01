# Editing the FM Dugout skin

This is a plain USS skin for **FM27 Launch Preview**. Edit a file, save it,
then reload or reapply the skin in FM. There is no build step, compiler or
plugin requirement.

`skin.json` loads `main.uss`, which imports the stylesheets directly. Broad
native defaults load first, followed by the theme, native variable mappings,
component rules, explicit utilities and finally `custom.uss`. Keep this order:
regrouping equally specific rules can change the result on controls that carry
several classes at once.

## Contents

- [What to edit](#what-to-edit)
- [Theme palette and global text](#theme-palette-and-global-text)
- [Surfaces, borders and corners](#surfaces-borders-and-corners)
- [Buttons, fields and selection](#buttons-fields-and-selection)
- [Navigation, bookmarks and menus](#navigation-bookmarks-and-menus)
- [Fonts and competition scoreboards](#fonts-and-competition-scoreboards)
- [Club and player headers](#club-and-player-headers)
- [Messages and news](#messages-and-news)
- [Tables, badges and data charts](#tables-badges-and-data-charts)
- [Tactics, recruitment and training](#tactics-recruitment-and-training)
- [Compact layout settings](#compact-layout-settings)
- [Match presentation](#match-presentation)
- [Light experiment and native limitations](#light-experiment-and-native-limitations)
- [Editing examples and checks](#editing-examples-and-checks)

## What to edit

| File | Purpose |
| --- | --- |
| `theme.uss` | Shared colours, text roles, fonts, control states, spacing settings and corner sizes |
| `theme-light.uss` | Optional Light palette experiment; disabled by default |
| `styles/navigation.uss` | Main/secondary navigation, bookmarks and header chrome |
| `styles/controls.uss` | Buttons, Continue, fields, dropdowns, toggles and their states |
| `styles/panels.uss` | Cards, frames, floating surfaces, image backplates and outlines |
| `styles/messages.uss` | Inbox/Portal rows, news, message details, conversations and attachments |
| `styles/typography.uss` | Heading/body utilities and component text exceptions |
| `styles/data.uss` | Tables, lists, attributes, charts and radar presentation |
| `styles/people.uss` | Clubs, players, staff, training, scouting and transfers |
| `styles/tactics.uss` | Pitches, positions, instructions and set pieces |
| `styles/match.uss` | Match, scoreboards, commentary and touchline presentation |
| `styles/screens.uss` | Calendar, preferences, setup, draft and other game pages |
| `styles/core.uss` | Shared helpers, spacing, layout and platform rules |
| `styles/fm-defaults.uss` | Advanced football/data palette and native fallback values |
| `styles/fm-contracts.uss` | FM's existing variable names mapped to the skin's tokens |
| `styles/utilities.uss` | Explicit spacing, layout and text helpers, loaded after component defaults |
| `custom.uss` | Personal overrides, imported last |

Start in `theme.uss` for a broad appearance change. Edit the relevant component
file for a particular page or control. `fm-contracts.uss` lets native FM
components consume the theme without renaming their existing variables.
`fm-defaults.uss` retains less common native and football-specific meanings.

## Theme palette and global text

| Tokens | Purpose |
| --- | --- |
| `--skin-surface-canvas` | Deepest canvas and ordinary top navigation |
| `--skin-surface-page` | Page workspace and neutral secondary navigation |
| `--skin-surface-navigation` | Separate navigation surface role |
| `--skin-surface-panel`, `--skin-surface-raised`, `--skin-surface-strong` | Panel layers and stronger neutral depth |
| `--skin-text-primary`, `--skin-text-secondary`, `--skin-text-disabled` | Ordinary, quieter and disabled copy |
| `--skin-text-link`, `--skin-text-link-hover` | USS-controlled link ink |
| `--skin-brand-primary`, `--skin-brand-primary-hover`, `--skin-brand-primary-pressed` | Main accent and its interaction states |
| `--skin-brand-on-primary` | Foreground paired with the main accent |
| `--skin-action-primary-*`, `--skin-selection-*` | Filled actions and selection, including foregrounds |
| `--skin-focus-ring` | Keyboard/open focus indication |
| `--skin-feedback-success-*`, `--skin-feedback-info-*`, `--skin-feedback-warning-*`, `--skin-feedback-danger-*` | Meaningful feedback foreground/surface pairs |
| `--skin-on-media`, `--skin-on-media-alpha-*` | Foregrounds and overlays for media, independent of ordinary page text |

Ordinary SIText enters through FM's `--global-text-primary` contract, mapped to
`--skin-text-primary`. Shared navigation, blocks and quieter labels consume the
corresponding ink roles. Keep these separate from surface colours and media
white: changing a panel fill should not redefine its text role.

Selection and accent roles follow the primary brand palette by default. You
can replace those aliases when designing a separate selection/accent scheme.
Keep Volt fills paired with dark action/selection ink through hover, press,
focus and disabled-selected states.

Colours use explicit RGB/RGBA values. When changing an opaque colour, update
the matching `-alpha-*` RGB channels in the final section of `theme.uss` too.
Changing only the opaque primary colour leaves some overlays on the old hue.
Aliases such as selection/accent alpha roles can still follow the primary
companions; inspect the final resolved chain before editing a second copy.

Preserve read/unread distinctions, disabled states, club identity, competition
colours, results, tactics and player status. These meanings should not all
collapse into the UI accent. Embedded rich-text names have a separate native
limitation described [below](#light-experiment-and-native-limitations).

## Surfaces, borders and corners

| Tokens | Purpose |
| --- | --- |
| `--skin-card-border-width`, `--skin-card-border-colour` | Ordinary report-card outlines |
| `--skin-dialog-surface`, `--skin-dialog-artwork`, `--skin-dialog-backdrop` | Floating dialog paint, optional decoration and outer backdrop |
| `--skin-dialog-border`, `--skin-dialog-border-width`, `--skin-dialog-radius` | Floating dialog edge and corners |
| `--skin-popup-radius`, `--skin-calendar-popup-radius` | Compact menu versus calendar corners |
| `--skin-radius-*` | Shared rectangular corner scale |
| `--skin-scrollbar-thumb`, `--skin-scrollbar-thumb-hover`, `--skin-scrollbar-thumb-pressed`, `--skin-scrollbar-radius` | SI/Unity scrollbar paint and shape |

Ordinary cards use surface depth, with a zero-width transparent outline by
default. Some native cards fix their border width inline; a transparent edge
can hide that paint without shifting content. For outlined cards, set both a
visible border colour and the desired width.

Floating dialogs have independent borders. Their native absolute border layer
sits beneath the content, so adding an edge does not consume the content's
padding. A border width of `0px` removes the outline. Compact popups use smaller
corners; calendars locally use their larger role so menu-row hover corners do
not become excessively round.

Popup chrome uses a plain dialog surface. `--skin-dialog-artwork: none` removes
its decorative frame artwork, while the transparent backdrop avoids a second
painted rectangle behind it. Photographs, icons and controller artwork remain
separate. Informational summary controls use `--skin-control-summary-*`; their
overlay-opacity role affects decorative paint rather than fading the contents.

Set applicable rectangular radius roles to `0px` for square controls/cards.
Joined edges stay square. Circular portraits, radio dots, chart markers and
pitch-position shapes retain their geometric roles. Unusual native corner sizes
may still need a component-specific review.

Empty `MenuBody`, `ReportBody`, reused full-window `Background` and match scene
hosts stay transparent. Visible page/report panels own the workspace fill.
Painting those hosts can cover the start-screen scene or the match renderer.
Scrollbar thumbs remain visible while idle when scrolling is available;
intentionally hidden or non-overflowing scrollers keep their native layout.

## Buttons, fields and selection

| Tokens | Purpose |
| --- | --- |
| `--skin-control-background`, `--skin-control-border`, `--skin-control-hover`, `--skin-control-pressed` | Neutral controls |
| `--skin-field-*` | Ordinary text-field surfaces, foregrounds, edges, focus and selection |
| `--skin-action-disabled-*` | Disabled action surface, border and foreground |
| `--skin-choice-background`, `--skin-choice-hover`, `--skin-choice-pressed`, `--skin-choice-foreground`, `--skin-choice-marker`, `--skin-choice-radius` | Plain form choices |
| `--skin-choice-card-*` | Larger neutral choice cards and compact title/description sizes |
| `--skin-radio-hover-background`, `--skin-radio-pressed-background`, `--skin-radio-interaction-foreground` | Radio pointer feedback |
| `--skin-radio-ring-foreground`, `--skin-radio-marker-foreground`, `--skin-radio-action-foreground` | Separate radio artwork roles |
| `--skin-switch-*` | On/off track and marker states |
| `--skin-range-track-background`, `--skin-range-track-border`, `--skin-range-marker*` | Slider tracks and handle states |
| `--skin-segmented-overlay-opacity` | Decorative selected-tab gradients |

Plain vertical form choices keep neutral rows and a Volt dot. Filled/segmented
choices use selection fill and paired dark ink. Hovering an unselected radio
must not make it look selected. Standalone checked checkboxes use Volt on the
small square and dark tick tint; disabled descendants retain native dimming.

FM can apply active and inactive classes to the same segmented control. The
selected rules deliberately outrank inactive defaults. Preserve that ordering
when editing hover/pressed rules, including nested text and monochrome glyphs.

Manager profile rows start neutral; their active class applies selection.
Manager-style/personality cards share a radius on their clipping wrapper and
painted frame, with a separate marker/tick. Appearance tabs' concept glyphs use
selection ink when filled. Portraits, clothing and other game artwork retain
their original tint. Detailed Preferences labels use secondary-navigation font
roles, and display-size glyphs use `--skin-preferences-scaling-icon-foreground`.

Text fields use the neutral field family. More specific focus rules preserve
the shared focus edge against native defaults. Text selection is translucent
because FM paints the highlight over selected glyphs. Numeric/error/warning
fields retain separate meanings.

Open secondary dropdowns remain neutral controls. Primary combobox labels and
chevrons pair with action ink. Default-validation fields, summary controls and
ownership/status pickers are separate families; do not make every open or
selected control a primary action.

Monochrome primary-action leaves use explicit action/disabled tint. A parent's
text colour does not necessarily tint a Unity image. Keep scopes narrow enough
to avoid recolouring club badges, portraits or arbitrary artwork. Colour-swatch
ticks use the supplied monochrome artwork under `assets/icons/`; the chosen
swatch colour remains game data.

## Navigation, bookmarks and menus

| Tokens | Purpose |
| --- | --- |
| `--skin-nav-active-indicator` | Primary and secondary navigation underlines |
| `--skin-nav-secondary-edge`, `--skin-nav-secondary-edge-width` | Divider beneath the secondary bar |
| `--skin-bookmark-*` | Bookmark backgrounds, state edges, text and overflow geometry |
| `--skin-menu-choice-*` | Detached dropdown rows |
| `--skin-menu-*`, `--skin-release-notes-*` | Start-screen typography, tiles, artwork and release-note layout |

Bookmarks use transparent resting fills and neutral hover/press feedback.
Keyboard/open focus keeps a separate edge. Their labels and overflow count
inherit secondary-navigation typography; the overflow glyph has its own centred
target. The secondary bar's frame owns one divider. Club identity strips and
separate club overview banners keep their native colours.

Detached dropdowns use quiet menu-choice roles. Cascading action menus retain
their own selected/action pairing. Hover and retained-highlight rules apply to
enabled rows; disabled choices keep their resting surface and disabled ink.
Pressed feedback follows hover in the cascade.

The start screen's small tiles share a heading/body scale; recent-career club
names retain a larger entity role. Release-note width, type, spacing and image
width are separate settings. Long release-note content scrolls within its
native dialog.

## Fonts and competition scoreboards

Loose font URLs resolve from the skin root, including URLs declared in imported
sheets: use `url("fonts/Poppins-Bold.ttf")`, not a parent-relative path.
Poppins Regular and Bold are included with their
[SIL Open Font License](fonts/OFL-Poppins.txt).

`--skin-font-family-primary`, `--skin-font-family-display` and
`--skin-font-family-navigation` own the main family choices. The
`--skin-font-secondary-navigation*`, `--skin-font-bookmark-label*`,
`--skin-font-primary-navigation*` and `--skin-font-section-heading*` roles allow
separate consumers. The independent `--skin-font-size-*` scale covers dense data,
headings and navigation. Larger text can expose native fixed-height/width limits.

The skin's own body/thematic/condensed aliases point to its chosen faces.
FM's original primary, thematic, condensed and international resources remain
game-owned. Competition-specific rules in `styles/match.uss` protect Premier
League, EFL, Bundesliga and UEFA scoreboard font families from general heading
rules. Generic/friendly scoreboards use the native primary font; authored bold
score/time leaves keep their native bold style. World Cup clock typography uses
the native international role; dynamic score/team choices remain game-owned.

UCL and UWCL roles reference `--ucl-family-regular` and `--uwcl-family-regular`.
No extracted UEFA font binaries are included. Native font outlines can differ
from their intended appearance; this public configuration needs an in-game check.
Changing the main skin font should not replace every competition's scorebug face.

## Club and player headers

| Tokens | Purpose |
| --- | --- |
| `--skin-club-summary-surface` | Translucent club banner summary cards |
| `--skin-club-details-scrim` | Backplate behind club title/metadata |
| `--skin-player-header-content-scrim` | Player identity/metadata backplate, separate from the portrait |
| `--skin-club-info-header-scrim`, `--skin-club-info-team-surface` | Club Info metadata and summary surfaces |
| `--skin-competition-summary-scrim` | Competition summary backplate |
| `--skin-header-gradient-extension`, `--skin-header-gradient-overlap` | Shared News/competition banner crop |
| `--skin-player-header-gradient-*`, `--skin-club-header-gradient-*` | Player and club crop aliases |
| `--skin-staff-header-gradient-*`, `--skin-team-report-header-gradient-*` | Horizontal staff/team-report crop |
| `--skin-player-header-horizontal-paint-scale`, `--skin-player-header-horizontal-content-scale` | Paint scaling and inverse content scaling |
| `--skin-contract-header-gradient-padding`, `--skin-contract-header-gradient-overlap` | Contract header paint extension with its native end inset |

Use alpha on summary-card/backplate fills rather than whole-card opacity. This
lets bound club colour show through while keeping text and icons crisp. The
player content scrim excludes its sibling portrait. Native club/competition
colours, kits and badges remain independent of UI branding.

Solid-looking banners extend the bound gradient beyond a clipped wrapper.
Extension and overlap pairs must remain equal and opposite; set both to `0px`
to restore that native fade. Contract headers retain a native `12px` end inset,
so their padding plus negative overlap must remain `12px`.

Some compact player headers bind width in game code and use paint/content
scales instead. Keep their product exactly one; setting both to `1` restores
the native fade. These settings extend paint while preserving content geometry.
Do not copy a crop rule blindly to a header with a different native structure.

Biography paragraphs use natural text growth. `--skin-biography-cover-gap`
separates cover artwork from the introduction; long biography scroll extent
still needs review. Milestone filter glyphs use selection/disabled ink without
recolouring timeline or club artwork.

## Messages and news

Inbox chrome uses `--skin-message-*` aliases for shared divider, surface, radius
and spacing roles. Structural attachments blend with the detail panel; semantic
data, response-required status and table stripes keep their own meanings.
Sender identity and the native club-colour edge are separate from decoration.

`--skin-text-read-opacity` and `--skin-text-read-selected-opacity` control read-tag
emphasis where FM exposes the disabled tag wrapper. Defaults are `0.55` at rest
and `0.65` when selected. A freshly opened retained row can keep an enabled tag
wrapper until the native list rebinds. USS cannot derive that state from sibling
read-text labels, so not every tag changes immediately with the headline.

Message/news banners clip to their shared radius while retaining bound club or
competition colour. Club news suppresses decorative texture rather than the
identity colour. Preparation sessions use dividers on the message surface.
Embedded report radars and legends use their own report-chart roles.

Targets, medical and scouting sections reuse structural attachment surfaces and
edges. Fixed-height medical descriptions ellipsize to avoid overlapping titles.
Scouting headers reuse the player paint/content scale pair and banner radius;
status colours, grade rings and native controls stay separate.

Reaction prose has a scoped wrapping rule that retains precedence when a generic
ellipsis utility is also present. Avoid changing card geometry or author labels
just to restore that prose wrap.

## Tables, badges and data charts

| Tokens | Purpose |
| --- | --- |
| `--skin-table-row-background`, `--skin-table-row-alternate-background`, `--skin-table-cell-background` | Stripes owned by the row rather than opaque cells |
| `--skin-list-selection-background`, `--skin-list-selection-foreground`, `--skin-list-selection-hover` | Neutral data-list selection |
| `--skin-badge-neutral-background`, `--skin-badge-neutral-foreground` | Informational badges |
| `--skin-notification-badge-background`, `--skin-notification-badge-foreground` | Filled count bubbles |
| `--skin-medical-risk-low-*`, `--skin-medical-risk-high-*` | Independent medical foreground/surface pairs |
| `--skin-grade-unknown-foreground` | Unknown/no-data information, separate from disabled controls |
| `--skin-chart-series-*`, `--skin-comparison-*` | Categorical charts and player comparison identities |
| `--skin-attribute-key*`, `--skin-attribute-preferred*`, `--skin-attribute-training*` | Attribute highlight ink and fills |
| `--skin-chart-compact-height`, `--skin-chart-report-radar-width` | Compact plots and report label gutters |
| `--skin-chart-first-contact-zone-height`, `--skin-chart-position-scrim` | Compact pitch labels and position-map backplates |
| `--skin-chart-radar-artwork`, `--skin-chart-compact-radar-background-size`, `--skin-chart-radar-label-min-width`, `--skin-chart-label-size` | Radar artwork and label layout |
| `--skin-radar-profile-line`, `--skin-radar-match-profile-line`, `--skin-report-radar-*` | Profile and embedded-report radar lines/fills |
| `--skin-chart-finance-*`, `--skin-finance-period-*`, `--skin-finance-category-*-colour` | Finance plots, period controls and category markers |

Selected rows retain child grade/status foregrounds. Avoid a blanket primary
colour on every selected descendant: pale/red badges may require dark text and
football colours must survive selection. Bound status/rating nodes named
`Background` retain their category fills; full-window hosts with the same name
have separate transparent rules.

Miniature form-bar lists use transparent chart backgrounds and
`--skin-form-bar-radius`. Full tables that also carry a `player-form-chart` class
keep ordinary stripes and interaction states. Chart geometry does not belong
to the same role as rectangular control corners.

Comparison uses separate left/right colours and translucent fills. Native
inline preferred-foot/height facts can keep their own colours; editing a chart
role changes only its stylesheet consumers. Semantic red/green progress fills
also retain their football feedback meaning when generic chart classes coexist.
Compound rules preserve that precedence after splitting the component sheets.

Radars use skin-root PNG artwork beneath the live polygon, with editable SVG
sources supplied alongside it. Compact Portal radars compensate for artwork
label padding through a background-size role; this scales only background paint,
not live series geometry. Full profile and comparison charts keep their own sizes.

Finance line/area/axis/gutter roles are independent of category markers and
native indexed pie palettes. Changing a Fund Raising/Other marker does not prove
a matching pie-slice change. Period tabs use neutral states and an outlined
selection because native bindings can keep their paint transparent. Dense chart
labels and season-table fitting remain areas to review.

## Tactics, recruitment and training

Tactics pitch/chrome uses `--skin-pitch-*` and `--skin-tactics-*`. Soften grass or
line paint without reducing a parent's opacity: kits, names and position marks
must stay crisp. Movement diagrams use opaque `--skin-tactics-movement-ip` and
`--skin-tactics-movement-oop`, separate from translucent attribute fills.

`--skin-player-number-*` owns number badge width, padding, type, paint and offset.
Picked-position hover/press overlays leave the bound position colour visible
underneath. Neutral tactical choices, opposition glyphs and penalty lists keep
separate scopes from miniature pitches and status symbols.

Squad Planner tiles use `--skin-planner-point-background`,
`--skin-planner-point-selected` and `--skin-planner-point-selected-border`.
Compact recruitment search pitches use `--skin-search-pitch-point-*` and
`--skin-search-pitch-label-size` instead of full planner geometry. Neutral
browse-card selection uses its own choice surface and accent outline; gold
assessment stars retain their meaning.

`--skin-recruitment-focus-count-grow` lets the count size to content while the
header details take spare width. Responsibility owner pickers use neutral
`--skin-responsibility-owner-*` surfaces/edges because native rich-person names
can retain white paint. Filled Volt needs actual rendered-name verification.
Detached owner dropdowns retain quiet menu-choice styling.

Training role fields and compact headers have their own insets. The intensity
fixture date stays on one line without replacing opponent-name ellipsis.
Attribute footers preserve horizontal padding while a separate vertical-inset
role controls their height. Low and High medical-risk badge pairs remain
separate from generic success/warning colours and unrelated rating scales.

## Compact layout settings

These settings recover room inside existing native columns/lanes. They do not
replace fonts, expand every table or guarantee that long localized copy fits.

| Tokens | Scope |
| --- | --- |
| `--skin-field-label-gap` | Checkbox/label separation, including Holiday's Jobs row |
| `--skin-facts-label-min-width` | Full Club Facts label lane and matching header spacer |
| `--skin-club-profile-value-max-width` | Compact Main Stadium value lanes |
| `--skin-summary-table-header-inset` | Compact Board, award-history and medical-risk headers |
| `--skin-training-table-header-inset`, `--skin-training-summary-dropdown-inset` | Training headers and leading-icon role fields |
| `--skin-training-traits-vertical-inset` | Individual Training Footedness/Traits footer |
| `--skin-match-summary-ratio-margin` | Compact TeamFormationAdaptive statistic text margins |
| `--skin-job-market-header-inset`, `--skin-job-market-competition-inset` | Vacancy headings and competition cells |
| `--skin-staff-job-gutter`, `--skin-staff-identity-portrait-gap` | Staff job/value separation and portrait/name gap |
| `--skin-captain-table-header-inset`, `--skin-number-table-plain-cell-inset` | Captains headers and Squad Numbers body text |
| `--skin-loans-expiry-text-trailing-gap`, `--skin-loans-expiry-cell-inset` | Loans expiry dates/NA text; clock spacing stays separate |
| `--skin-manager-history-record-group-gap`, `--skin-manager-history-record-label-gap`, `--skin-manager-history-tile-name-max-width` | History record spacing and compact tile name lane |
| `--skin-finance-budget-action-trailing-gap`, `--skin-finance-breakdown-view-min-width` | Budget open-icon gap and authored Expenditure season view |
| `--skin-preferences-compact-help-size` | Compact Preferences Saves-tile help |
| `--skin-player-training-summary-size`, `--skin-attribute-label-line-height` | Compact assessment copy and attribute-link descenders |

Keep adjacent gutters, sort-icon gaps, row heights and body-cell allocation
separate when reducing one inset. A change that fixes one heading can steal
space from its neighbour. Some long staff jobs, Board dates, finance charts and
small-screen labels may still truncate; check the actual text at your UI scale.

## Match presentation

Matchday retains its native paper team sheet and dark text through
`--skin-match-sheet-*`. A supplied one-pixel mask, tinted by the theme, covers
specific surrounding inline card surfaces without replacing club stripes, kits
or competition artwork. Paper-sheet rows remain transparent independently of
ordinary dark table stripes.

The full-window host and live-match HUD stay transparent for the 3D renderer.
The between-highlights dashboard uses the native conditional background that
FM hides during highlights. `--skin-match-overview-card-background` supplies
ordinary centre-viewer and squad-strip cards; ratings, kit art and statuses keep
their native paint. Header chrome can float over the scene while ordinary main
navigation keeps its canvas fill.

Half/full-time report gaps reveal the stadium, with solid report cards above.
Their reused image frame suppresses its own bound backdrop, leaving the native
layout visible. Floating player profiles reuse profile radar artwork/outline,
header paint scaling and selected toggle ink. These scopes must not turn the
entire match renderer opaque.

Playback glyphs use action ink. Live highlight-choice radios reuse the neutral
vertical-choice contract without changing native pie-gauge art. Meeting answer
cards keep light body copy separate from filled action tags.

## Light experiment and native limitations

Dark is the default. To preview the optional Light file, add this import
immediately after the `theme.uss` import in `main.uss`:

```uss
@import url("theme-light.uss");
```

Remove that line to return to Dark. The override changes existing palette roles
for surfaces, ordinary text, links, controls, actions, focus and feedback. Font,
geometry, media whites and native football/data colours keep their separate
owners. The preserved data palette still has insufficient contrast on some
light surfaces, so Light is an experiment rather than a finished supported skin.

In FM27 Launch Preview, some embedded club/player names are formatted with
explicit native rich-text colours. A label can have the correct computed USS
foreground while those spans remain white. This was also reproduced outside
the Dugout skin; no loose-USS palette override has been verified. The game's
hyperlink-highlighting preference is not a verified fix for this colour source.

Adaptive club-header text uses a separate game-bound contrast colour. That
behaviour does not establish a global USS hook for embedded body links.
Ownership/status pickers and selected controls containing those names need
readable surfaces even when the ordinary USS foreground has changed.

USS also cannot infer every state from a neighbouring element, and native
bindings can own dimensions, colours or text independently. Not every page,
resolution, language or pointer/focus state is verified. Changes to native font
resolution and full match-stage rendering need their own visual checks.

## Editing examples and checks

Use `custom.uss` for personal overrides rather than repeating a selector in
several component files. This example changes only existing theme roles:

```uss
:root {
  --skin-card-border-width: 1px;
  --skin-card-border-colour: var(--skin-border-subtle);
  --skin-dialog-border-width: 0px;
}
```

It enables ordinary report-card edges and removes the independent floating
outline. To restore the default card treatment, use width `0px` and colour
`var(--skin-transparent)`; restore the dialog border width to `1px`.

For a broader theme change, edit the appropriate values in `theme.uss`, or add
a separate token-only override after that file and before `styles/fm-contracts.uss`.
Keep the full state palette and alpha companions together. Do not replace native
football/data contracts with one brand colour.

After saving, reload or reapply the skin and inspect an ordinary page, a table,
a popup, a coloured club/player header and any affected match UI. Check selected,
hovered, pressed, disabled and keyboard-focus states, plus long names and a
lighter club identity. Verify that photographs, club badges, chart meanings and
match rendering remain intact. Keep a backup before replacing an installed copy.

Source parsing or a successful reload alone does not establish that every
binding, screen and interaction state renders correctly. Installation paths and
public support boundaries are in the
[repository README](https://github.com/lotsgon/fm27-dugout-skin-public#readme).
