# ClariFact — Product Requirements Document (PRD)

## 7.1 Product Overview

**ClariFact** is an AI-powered multimodal content credibility analysis system. It allows authenticated users to submit text, images, or short videos for AI-assisted credibility and content analysis. The system processes the submitted content, extracts checkable claims, retrieves supporting or contradicting evidence, and produces an explainable credibility assessment with a score, confidence level, claim breakdown, and evidence sources.

The system does **not** claim to determine absolute truth. It provides an AI-assisted credibility assessment that helps users understand the likelihood and quality of claims within their content.

## 7.2 Problem Statement

Modern internet users are overwhelmed with text, images, and videos containing claims, opinions, and misinformation. The problems include:

- **Misinformation**: False or misleading content spread unintentionally.
- **Unsupported Claims**: Statements made without evidence.
- **Verification Difficulty**: Average users cannot easily verify content credibility.
- **Multimodal Content**: Text can be extracted, but images and videos require OCR, transcription, and visual analysis — creating a fragmented verification experience.
- **Lack of Explainability**: Many AI systems output binary "true/false" without reasoning, leaving users unsure why an assessment was made.

ClariFact addresses these by providing a unified platform that handles all input modalities, extracts claims, retrieves evidence, and presents assessments with full explainability.

## 7.3 Product Vision

To become the go-to tool for internet users who want to quickly understand the credibility and quality of digital content they encounter. ClariFact aims to democratize access to credibility assessment through an explainable, multimodal system that works for students, researchers, educators, journalists, and general content consumers.

## 7.4 Target Users

- **Students**: Verify sources for essays and research papers.
- **Researchers**: Quickly assess credibility of claims in papers or articles.
- **General Internet Users**: Check the credibility of viral content, social media posts, or news.
- **Content Consumers**: Understand the quality and trustworthiness of videos, images, and articles they consume.
- **Educators**: Teach media literacy and source evaluation.
- **Journalists/Researchers**: Perform initial credibility checks on sources and claims.

## 7.5 Core Features

1. **Authentication**: Registration, login, logout, protected dashboard, user-specific history.
2. **Text Analysis**: Preprocessing, claim extraction, evidence retrieval, credibility assessment, content quality analysis, report generation.
3. **Image Analysis**: Upload, validation, OCR, text extraction, claim extraction, evidence retrieval, credibility assessment, visual analysis, report generation.
4. **Video Analysis**: Upload, validation, audio extraction, speech-to-text, transcript, claim extraction, evidence retrieval, credibility assessment, frame sampling, visual analysis, content quality analysis, report generation.
5. **Analysis History**: View previous analyses, detail view, source display.
6. **User Dashboard**: Central hub for managing analyses and settings.

## 7.6 Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-AUTH-001 | The system shall allow a user to register with name, email, and password. |
| FR-AUTH-002 | The system shall authenticate registered users. |
| FR-AUTH-003 | The system shall provide a logout function. |
| FR-AUTH-004 | The system shall provide an authenticated dashboard accessible only to logged-in users. |
| FR-AUTH-005 | Every analysis shall belong to an authenticated user. |
| FR-AUTH-006 | Users must never be able to access another user's private analyses. |
| FR-CONT-001 | The system shall accept text content input. |
| FR-CONT-002 | The system shall accept image file uploads (JPEG, PNG, WebP). |
| FR-CONT-003 | The system shall accept short video file uploads (MP4, WebM, MOV). |
| FR-CONT-004 | Image uploads shall be validated for size and format. |
| FR-CONT-005 | Video uploads shall be validated for size, duration, and format. |
| FR-ANALYSIS-001 | The system shall extract checkable claims from text content. |
| FR-ANALYSIS-002 | The system shall extract text from images via OCR. |
| FR-ANALYSIS-003 | The system shall extract text from video via speech-to-text. |
| FR-EVIDENCE-001 | The system shall retrieve relevant supporting or contradicting evidence for claims. |
| FR-CREDIBILITY-001 | The system shall produce a credibility score (0-100) and label. |
| FR-CREDIBILITY-002 | The system shall assess claim-level support (Supported, Partially Supported, Uncertain, Potentially Misleading). |
| FR-QUALITY-001 | The system shall analyze content quality characteristics. |
| FR-REPORT-001 | The system shall generate an explainable report with assessment, confidence, claims, and evidence. |
| FR-HISTORY-001 | The system shall store analyses user-specifically and provide history listing. |
| FR-HISTORY-002 | The system shall provide analysis detail view with full report. |
| FR-HISTORY-003 | The system shall display sources/evidence associated with each analysis. |

## 7.7 Non-Functional Requirements

- **Security**: Passwords must be hashed using bcrypt. JWT or session tokens for authentication. All backend endpoints must be protected. Input validation on all user inputs. CORS configuration for production. Environment variables for secrets. SQL injection protection via parameterized queries/ORM.
- **Performance**: Text analysis should complete within 10 seconds for typical content. Image analysis within 15 seconds. Video analysis within 30 seconds for videos up to 5 minutes. Evidence retrieval should not block the main thread.
- **Reliability**: System should gracefully handle malformed inputs, unsupported formats, and extraction failures. Fallback responses for images with little readable text.
- **Maintainability**: Code must follow modular architecture. Documentation must stay synchronized with implementation. Clear separation of concerns between frontend, backend, AI/ML, and database layers.
- **Usability**: Interface must be clean, modern, and intuitive. Error messages should be helpful, not technical. Loading states must be displayed during AI processing. Results must be easy to read and understand.
- **Scalability**: Database schema must support growing number of users and analyses. AI models should be loadable without restart. Evidence retrieval should be designed for horizontal scaling.
- **Accessibility**: Web interface should meet WCAG 2.1 AA standards. Color contrast sufficient. Keyboard navigable. Alternative text for images.
- **Privacy**: User data (analyses, history) must be isolated per user. No plaintext passwords. Minimal data retention. Clear privacy policy for AI processing.

## 7.8 Scope (MVP)

**In Scope:**
- User registration, login, logout, and authenticated dashboard.
- Text analysis pipeline: preprocessing → claim extraction → evidence retrieval → credibility assessment → report.
- Image analysis pipeline: upload → validation → OCR → claim extraction → evidence retrieval → credibility → report.
- Video analysis pipeline: upload → validation → audio extraction → speech-to-text → transcript → claim extraction → evidence retrieval → credibility → report.
- Analysis history with detail view.
- Credibility scoring with claim-level breakdown (Supported/Partially Supported/Uncertain/Potentially Misleading).
- Explainable reports with evidence sources.

**Out of Scope (Future):**
- Browser extension.
- Mobile application.
- Advanced deepfake detection.
- Real-time video processing.
- Multi-language support beyond English.
- Social media integration.
- Collaborative analysis features.

## 7.9 Limitations

- AI can make mistakes; credibility is an assessment, not absolute truth.
- Evidence retrieval may be incomplete; some claims cannot be verified automatically.
- Sources may disagree on claim validity.
- Credibility scores are based on available evidence at the time of analysis and may change as new evidence emerges.
- Image OCR accuracy depends on image quality, lighting, and text clarity.
- Video transcription accuracy depends on audio quality, speaker accent, and background noise.
- The system processes short videos only (defined maximum duration and file size).
- Model predictions are based on patterns in training data and may not generalize to all domains.

## 7.10 Future Enhancements

- More languages and locale-aware claim extraction.
- Browser extension for on-the-page analysis.
- Mobile application for on-device analysis.
- Advanced deepfake and manipulated media analysis.
- More sophisticated visual understanding (diagrams, charts, tables).
- More sophisticated source ranking and credibility weighting.
- User-saved favorite sources.
- Collaborative annotation and discussion.

*Future features will be implemented after MVP launch and based on user feedback.*