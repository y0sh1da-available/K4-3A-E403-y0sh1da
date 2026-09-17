import json
import time
from pathlib import Path
import sys

# Thêm thư mục backend vào sys.path để import app
BACKEND_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BACKEND_DIR))

from app.schemas import ChatRequest
from app.services.tutor_service import handle_chat

def main():
    root_dir = BACKEND_DIR.parents[1] if (BACKEND_DIR.parents[1] / 'eval').exists() else BACKEND_DIR.parent.parent
    golden_set_path = root_dir / 'eval' / 'golden_set.json'
    
    if not golden_set_path.exists():
        # Thử tìm tương đối
        golden_set_path = Path('eval/golden_set.json')
        if not golden_set_path.exists():
            print(f'Error: Không tìm thấy file {golden_set_path}')
            return

    with open(golden_set_path, 'r', encoding='utf-8') as f:
        cases = json.load(f)

    print('=' * 80)
    print(f'🚀 BẮT ĐẦU CHẠY EVALUATION BỘ GOLDEN SET ({len(cases)} CA KIỂM THỬ)')
    print('=' * 80)

    passed = 0
    failed = 0
    results = []
    
    log_dir = BACKEND_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'eval.log'

    with open(log_file, 'a', encoding='utf-8') as log_f:
        log_f.write(f'\n--- EVAL RUN: {time.strftime(\"%Y-%m-%d %H:%M:%S\")} ---\n')

        for i, c in enumerate(cases, 1):
            req = ChatRequest(
                user_input=c['user_input'],
                slide_context=c['slide_context'],
                slide_page=c['slide_page']
            )

            start_t = time.time()
            try:
                resp = handle_chat(req)
                latency_ms = int((time.time() - start_t) * 1000)
                is_match = (resp.case == c['expected_case'])

                if is_match:
                    passed += 1
                    status = '✅ PASS'
                else:
                    failed += 1
                    status = '❌ FAIL'

                print(f'[{i:02d}/20] {status} | Case: {c[\"id\"]} ({c[\"layer\"]})')
                print(f'     User: \"{c[\"user_input\"]}\"')
                print(f'     Kỳ vọng: {c[\"expected_case\"]} ({c[\"expected_action\"]}) -> Thực tế: {resp.case} ({resp.action}) [{latency_ms}ms]')
                if not is_match:
                    print(f'     ⚠️ Lý do: Model trả về {resp.case}, phản hồi: \"{resp.reply_text[:60]}...\"')
                print('-' * 80)

                log_entry = {
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'case_id': c['id'],
                    'user_input': c['user_input'],
                    'expected': c['expected_case'],
                    'actual': resp.case,
                    'is_pass': is_match,
                    'latency_ms': latency_ms,
                    'reply_text': resp.reply_text
                }
                log_f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

            except Exception as e:
                failed += 1
                print(f'[{i:02d}/20] ❌ ERROR | Case: {c[\"id\"]}: {e}')
                print('-' * 80)

    total = passed + failed
    accuracy = (passed / total * 100) if total > 0 else 0
    print('=' * 80)
    print(f'📊 KẾT QUẢ EVALUATION CUỐI CÙNG:')
    print(f'   - Tổng số test cases: {total}')
    print(f'   - Số ca đạt chuẩn: {passed}')
    print(f'   - Số ca chưa đạt: {failed}')
    print(f'   - ĐỘ CHÍNH XÁC (ACCURACY): {accuracy:.1f}%')
    print(f'   - File log chi tiết đã lưu tại: {log_file}')
    print('=' * 80)

if __name__ == '__main__':
    main()
