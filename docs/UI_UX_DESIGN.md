# ClariFact — UI/UX Design Specification (UI_UX_DESIGN.md)

## Design Principles

The design should be:
- **Modern**: Clean lines, contemporary aesthetics.
- **Clean**: Ample white space, clear hierarchy.
- **Trustworthy**: Professional colors, consistent branding.
- **Professional**: Suitable for academic, research, and general use.
- **Accessible**: WCAG 2.1 AA compliant, keyboard navigable.
- **Responsive**: Works on mobile, tablet, and desktop.

## Typography

**Primary Font**: `Athelas` (serif, for headings and serious content)

**Fallback Fonts**: Georgia, Times New Roman, serif

**Accent Font**: `Vanguard` (sans-serif, for UI elements, buttons, modern look)

**Fallback Fonts**: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif

> Note: Do not commit unlicensed font files. Use system fonts or web-safe fonts in production. Athelas and Vanguard are specified for design spec; implementation should use appropriate open-source alternatives or system fonts.

## Color Palette

| Color | Hex | Usage |
|---|---|---|
| `--bg-light` | `#f8f9fa` | Background pages/surfaces |
| `--bg-card` | `#ffffff` | Cards, modals, result boxes |
| `--bg-muted` | `#e9ecef` | Disabled inputs, borders |
| `--text-primary` | `#212529` | Primary text |
| `--text-secondary` | `#6c757d` | Secondary text, metadata |
| `--accent-primary` | `#3b82f6` | Primary actions, links |
| `--accent-secondary` | `#10b981` | Secondary actions, success states |
| `--accent-warning` | `#f59e0b` | Warnings, partially supported claims |
| `--accent-danger` | `#ef4444` | Potentially misleading, errors |
| `--border` | `#d1d5db` | Input borders, dividers |

> Credibility scores must NOT use red/green color blindness dependent indicators alone. Use text labels (✓, ⚠, ?) alongside colors.

## Pages

### 1. Landing / Home

- **Purpose**: Introduce ClariFact, explain purpose, encourage signup/login.
- **Layout**:
  - Hero section with headline: "AI-Powered Multimodal Content Credibility Analysis"
  - Subheadline: "Submit text, images, or short videos to understand claim credibility."
  - Three feature cards: Text, Image, Video analysis.
  - Login/Register CTA buttons.
- **Components**: Hero, FeatureCard, CTAButton, SocialProof (optional).
- **User Actions**: Click "Login", click "Register", click feature cards.
- **Validation**: None.
- **Loading States**: None.
- **Error States**: None.
- **Responsive**: Full width hero on mobile, 2-column on tablet, 3-column on desktop.

### 2. Login

- **Purpose**: Authenticate existing users.
- **Layout**: Centered form card on bg-light.
  - Email input with icon.
  - Password input with icon.
  - "Forgot password?" link (future).
  - Login CTA.
  - Register link: "Don't have an account? Register."
- **Components**: Form, Input, Label, Button, Link.
- **User Actions**: Enter credentials, click login.
- **Validation**: Required fields, email format.
- **Error States**: Invalid credentials shown below form.
- **Loading States**: "Logging in..." button state.
- **Responsive**: Full width card, centered.

### 3. Register

- **Purpose**: Create new user account.
- **Layout**: Similar to Login form.
  - Name input.
  - Email input.
  - Password input.
  - Password confirmation input.
  - Register CTA.
  - Login link: "Already have an account? Login."
- **Components**: Same as Login.
- **User Actions**: Enter details, click register.
- **Validation**: All required, password match, email format, unique email.
- **Error States**: Email already taken, passwords don't match.
- **Loading States**: "Creating account..." button state.
- **Responsive**: Same as Login.

### 4. Dashboard

- **Purpose**: Main hub; list analyses, start new analysis.
- **Layout**:
  - Topbar: User profile menu, logout button.
  - Main content area:
    - Section: "Recent Analyses" (list of cards).
    - Section: "Start New Analysis" (tabs: Text, Image, Video).
  - Sidebar/navigation: Home, Dashboard, History, Settings.
- **Components**: Topbar, AnalysisCard, TabButton, NavMenu.
- **User Actions**: Click analysis card to view detail, click "New Analysis" tab, click logout.
- **Validation**: None.
- **Loading States**: "Loading analyses..." spinner.
- **Error States**: "Could not load analyses. Please try again."
- **Responsive**: Sidebar hides on mobile, becomes bottom nav.

### 5. Analyze (Content Submission)

- **Purpose**: User selects content type and submits.
- **Layout**: Tabbed interface (Text / Image / Video).
  - **Text Tab**: Textarea, "Analyze" button.
  - **Image Tab**: File input (accept: image/*), preview, "Analyze" button.
  - **Video Tab**: File input (accept: video/*), preview, duration info, "Analyze" button.
- **Components**: TabbedForm, Textarea, FileInput, PreviewImage/Video, Button.
- **User Actions**: Select content type, upload file or paste text, click Analyze.
- **Validation**: Non-empty, file type/size limits.
- **Loading States**: "Analyzing..." button state, full-screen spinner over analysis area.
- **Error States**: "Invalid content. Please check format and try again."
- **Responsive**: Tabs stack vertically on mobile.

### 6. Processing

- **Purpose**: Show AI pipeline in progress.
- **Layout**: Centered overlay with:
  - Spinner/animation.
  - Progress text: "Analyzing... (Claim extraction → Evidence retrieval → Credibility assessment)".
  - Optional: modality-specific progress (e.g., "OCR in progress...").
- **Components**: Spinner, ProgressText.
- **User Actions**: None (wait).
- **Loading States**: Full duration of AI processing.
- **Error States**: "Analysis failed. Please try again."
- **Responsive**: Centered, covers available area.

### 7. Results

- **Purpose**: Display credibility assessment report.
- **Layout**: Main result card on bg-card with:
  - **Overall Credibility**: Large score (e.g., "84/100") with label ("Mostly Credible").
  - **Assessment**: Text below score.
  - **Confidence**: Progress bar or percentage ("88%").
  - **Claims Detected**: Three subsections:
    - ✓ Supported (list)
    - ⚠ Partially Supported (list)
    - ? Uncertain (list)
  - **Content Quality**: 
    - Speech Quality (if video/audio).
    - Visual Quality (if image).
    - Content Relevance.
    - Engagement Indicators.
  - **Evidence / Sources**: List of sources with links/snippets.
  - **AI Explanation**: Paragraph text explaining the assessment.
- **Components**: ResultCard, ScoreBadge, ClaimList, QualityGrid, SourceList, ExplanationText.
- **User Actions**: Read report, click source links (open in new tab), "Analyze New", view in history.
- **Validation**: None (read-only).
- **Loading States**: Not applicable (result displayed).
- **Error States**: "No analysis found."
- **Responsive**: Card stacks full width on mobile, narrower on desktop with sidebar.

> **Important**: The credibility score must NOT visually look like guaranteed truth. Use "Overall Credibility: 84/100" with label text, not as a guarantee. Colors should be informational (e.g., blue, not traffic-light green/red alone).

### 8. History

- **Purpose**: List user's previous analyses.
- **Layout**: List of analysis cards, each showing:
  - Date/time.
  - Content type icon (T / I / V).
  - Credibility score label.
- **Components**: AnalysisList, AnalysisCard.
- **User Actions**: Click card to view detail, swipe/delete to remove.
- **Loading States**: "Loading history..." spinner.
- **Error States**: "Could not load history."
- **Responsive**: List stacks on mobile.

### 9. Analysis Detail

- **Purpose**: Full report view for a specific analysis.
- **Layout**: Same as Results page but for a single stored analysis.
- **Components**: Same as Results.
- **User Actions**: Read report, delete analysis, share results.
- **Responsive**: Same as Results.

### 10. Error / Empty States

- **404 Not Found**: Friendly page with link back to dashboard.
- **Empty History**: "No analyses yet. Start by analyzing your first text, image, or video."
- **Empty Search/Results**: "No claims found or evidence unavailable. The analysis may have limited claims."
- **Design**: Consistent with overall design language, includes illustrative graphic or icon and CTA.

## Results UI Specification (Detailed)

```text
Overall Credibility: 84/100

Assessment:
Mostly Credible

Confidence:
88%

Claims Detected
✓ Supported
  - Claim 1 text...
  - Claim 2 text...
⚠ Partially Supported
  - Claim 3 text...
? Uncertain
  - Claim 4 text...

Content Quality
Speech Quality: Good / Poor / N/A
Visual Quality: Good / Poor / N/A
Content Relevance: High / Medium / Low
Engagement Indicators: (metrics)

Evidence / Sources
Source 1: [Title/Link]
Source 2: [Title/Link]
Source 3: [Title/Link]

AI Explanation:
The majority of detected claims are supported by
available evidence. One claim could not be
sufficiently verified.
```

- Use `✓`, `⚠`, `?` emoji/tokens with text labels.
- Do NOT use traffic-light colors as sole indicators.
- Credibility score in large typography but with supporting label text.
- Confidence as percentage with progress bar (discreet, not gamified).
- Sources displayed as clickable items.
- AI explanation in paragraph form, not bulletless.

## Accessibility Notes

- Color contrast: `--text-primary` on `--bg-light` >= 4.5:1.
- Focus outlines on interactive elements.
- Alt text for all icons and decorative images.
- Keyboard: Tab order through form elements, Enter activates buttons.
- Screen reader: Landmark regions (header, main, nav, aside, footer).
- Text resize: Page zoom up to 200% should not break layout.
- Reduced motion: Respect `prefers-reduced-motion`; spinner may be static.

## Responsive Behavior

| Breakpoint | Width | Layout Changes |
|---|---|---|
| Mobile | < 640px | Full-width cards, stacked columns, bottom nav. |
| Tablet | 640px - 1024px | 2-column grids, sidebar collapsible. |
| Desktop | > 1024px | 3-column grids, persistent sidebar, wider result cards. |

> All breakpoints should test: header, nav, forms, result cards, modals.