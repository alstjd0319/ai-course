```markdown
# 1. 개요
사용자가 할 일을 간단하게 기록하고 관리할 수 있는 웹 애플리케이션입니다. 최소한의 속성만을 사용하여 직관적이고 빠른 사용성을 제공하는 것을 목표로 합니다.

# 2. 기술
- **Language**: Python 3.x
- **Framework**: Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3 (Pure CSS)

# 3. 파일 구성
- `app.py`: Flask 애플리케이션 메인 로직 및 라우팅
- `database.db`: SQLite 데이터베이스 파일
- `schema.sql`: 데이터베이스 테이블 생성 스크립트
- `static/style.css`: 애플리케이션 디자인을 위한 CSS 파일
- `templates/index.html`: 할 일 목록 및 입력 폼을 포함한 메인 페이지 템플릿

# 4. 동작 규칙

| 라우트 | 메서드 | 입력 | 결과 |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | 없음 | 전체 할 일 목록을 포함한 메인 페이지 렌더링 |
| `/add` | `POST` | `title` (문자열) | 새로운 할 일 추가 후 메인 페이지로 리다이렉트 |
| `/toggle/<int:todo_id>` | `POST` | `todo_id` (정수) | 해당 ID의 완료 상태(`is_completed`)를 반전시킨 후 리다이렉트 |
| `/delete/<int:todo_id>` | `POST` | `todo_id` (정수) | 해당 ID의 데이터를 삭제한 후 메인 페이지로 리다이렉트 |

# 5. 화면
- **메인 페이지**:
    - 상단: 새로운 할 일을 입력할 수 있는 입력창과 '추가' 버튼
    - 중앙: 할 일 목록 (최근 생성된 순서대로 표시)
        - 미완료 항목: 일반 텍스트로 표시
        - 완료 항목: 취소선(strikethrough) 적용 및 시각적 구분
    - 항목별 액션: 각 항목 옆에 '완료/해제' 버튼과 '삭제' 버튼 배치

# 6. 테스트

| 요청 | 기대하는 결과 |
| :--- | :--- |
| `GET /` | 200 OK 및 빈 목록 또는 기존 목록 페이지 출력 |
| `POST /add` (유효한 `title`) | 302 Redirect 후 데이터베이스에 항목 저장 확인 |
| `POST /add` (빈 문자열 `title`) | 302 Redirect 혹은 에러 처리 (데이터 저장되지 않음) |
| `POST /add` (공백만 있는 `title`) | 302 Redirect 혹은 에러 처리 (데이터 저장되지 않음) |
| `POST /add` (매우 긴 문자열) | DB 제약 조건에 따른 처리 혹은 정상 저장 |
| `POST /toggle/1` (존재하는 ID) | 302 Redirect 후 해당 항목의 `is_completed` 상태 변경 확인 |
| `POST /toggle/999` (존재하지 않는 ID) | 404 Not Found 혹은 에러 발생 |
| `POST /delete/1` (존재하는 ID) | 302 Redirect 후 데이터베이스에서 해당 항목 삭제 확인 |
| `POST /delete/999` (존재하지 않는 ID) | 404 Not Found 혹은 에러 발생 |
| `POST /delete/-1` (잘못된 형식의 ID) | 404 Not Found 혹은 라우팅 오류 발생 |

# 7. 완료 전 점검
- [ ] 모든 할 일은 생성 시 자동으로 현재 시각이 기록되는가?
- [ ] 할 일 목록은 최신 항목이 가장 위에 나타나는가?
- [ ] 완료 버튼을 누르면 즉시 취소선이 적용되어 화면에 반영되는가?
- [ ] 삭제 버튼을 누르면 목록에서 즉시 사라지는가?
- [ ] SQLite 파일이 정상적으로 생성되고 데이터가 유지되는가?

# 8. 하지 않는 것
- 사용자 인증 (로그인/회원가입) 기능
- 할 일 내용 수정 (Edit) 기능
- 외부 CSS 프레임워크 사용 (Bootstrap, Tailwind 등)
- JavaScript 프레임워크 사용 (React, Vue 등)
- AJAX를 이용한 비동기 통신 (모든 요청은 SSR 방식으로 처리)
```