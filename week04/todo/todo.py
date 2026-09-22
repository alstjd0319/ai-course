import json
import os
from datetime import datetime

class TodoManager:
    def __init__(self, filename='todo.json'):
        self.filename = filename
        self.todos = self._load_todos()

    def _load_todos(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_todos(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"파일 저장 중 오류가 발생했습니다: {e}")

    def add_todo(self, task, deadline):
        self.todos.append({
            'task': task,
            'completed': False,
            'deadline': deadline
        })
        self._save_todos()
        print(f"'{task}' (마감일: {deadline}) 할 일이 추가되었습니다.")

    def list_todos(self):
        if not self.todos:
            print("\n현재 할 일 목록이 비어 있습니다.")
            return

        # 마감일 기준으로 정렬 (날짜 문자열 형식이 YYYY-MM-DD 이므로 문자열 정렬 가능)
        sorted_todos = sorted(self.todos, key=lambda x: x.get('deadline', '9999-12-31'))

        print("\n--- 할 일 목록 (마감일 순) ---")
        for index, todo in enumerate(sorted_todos, start=1):
            status = "[V]" if todo['completed'] else "[ ]"
            deadline = todo.get('deadline', '미정')
            print(f"{index}. {status} {todo['task']} (마감: {deadline})")
        print("------------------------------")
        
        # 정렬된 목록의 인덱스를 실제 todos 리스트와 매핑하기 위해 
        # 여기서는 간단하게 sorted_todos를 반환하거나, 
        # 사용자가 선택한 번호가 실제 리스트의 어디인지 찾는 로직이 필요합니다.
        # 편의를 위해 list_todos는 출력만 하고, 실제 index 처리는 별도로 구성하겠습니다.
        return sorted_todos

    def complete_todo(self, sorted_list, target_index):
        try:
            # sorted_list에서 선택된 아이템을 찾아 실제 todos 리스트에서 업데이트
            item_to_complete = sorted_list[target_index - 1]
            for todo in self.todos:
                if todo == item_to_complete:
                    todo['completed'] = True
                    break
            self._save_todos()
            print(f"'{item_to_complete['task']}' 할 일을 완료로 표시했습니다.")
        except (IndexError, KeyError):
            print("잘못된 번호입니다.")

    def delete_todo(self, sorted_list, target_index):
        try:
            item_to_delete = sorted_list[target_index - 1]
            self.todos.remove(item_to_delete)
            self._save_todos()
            print(f"'{item_to_delete['task']}' 할 일이 삭제되었습니다.")
        except (IndexError, ValueError):
            print("잘못된 번호입니다.")

def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def main():
    manager = TodoManager()

    while True:
        print("\n=== 할 일 관리 프로그램 ===")
        print("1. 할 일 추가")
        print("2. 목록 보기")
        print("3. 완료 표시")
        print("4. 삭제")
        print("5. 종료")
        
        choice = input("메뉴를 선택하세요 (1-5): ").strip()

        if choice == '1':
            task = input("추가할 할 일을 입력하세요: ").strip()
            if not task:
                print("할 일 내용은 비어 있을 수 없습니다.")
                continue
            
            deadline = input("마감일을 입력하세요 (YYYY-MM-DD) 또는 엔터 시 미정: ").strip()
            if deadline:
                if validate_date(deadline):
                    manager.add_todo(task, deadline)
                else:
                    print("날짜 형식이 잘못되었습니다. YYYY-MM-DD 형식을 사용하세요.")
            else:
                manager.add_todo(task, "미정")
        
        elif choice == '2':
            manager.list_todos()

        elif choice == '3':
            sorted_list = manager.list_todos()
            if sorted_list:
                try:
                    index = int(input("완료로 표시할 번호를 입력하세요: "))
                    manager.complete_todo(sorted_list, index)
                except ValueError:
                    print("숫자를 입력해주세요.")

        elif choice == '4':
            sorted_list = manager.list_todos()
            if sorted_list:
                try:
                    index = int(input("삭제할 번호를 입력하세요: "))
                    manager.delete_todo(sorted_list, index)
                except ValueError:
                    print("숫자를 입력해주세요.")

        elif choice == '5':
            print("프로그램을 종료합니다.")
            break
        
        else:
            print("잘못된 선택입니다. 다시 시도해주세요.")

if __name__ == "__main__":
    main()
