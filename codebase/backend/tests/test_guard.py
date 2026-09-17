import unittest

from app.schemas import (
    ChatRequest,
    ChatResponse,
    Citation,
)

from app.services.tutor_service import (
    BackendValidationError,
    validate_response,
)


class TestGroundingGuard(unittest.TestCase):

    def setUp(self):
        self.request = ChatRequest(
            user_input="Data Lake là gì?",
            slide_context=(
                "Data Lake là một kho lưu trữ dữ liệu "
                "tập trung, quy mô lớn."
            ),
            slide_page=12,
        )

    def test_valid_citation_passes(self):

        response = ChatResponse(
            case="A",
            action="ANSWER_WITH_CITATION",
            reply_text=(
                "Data Lake là một kho lưu trữ "
                "dữ liệu tập trung."
            ),
            citation=Citation(
                has_citation=True,
                source="Slide 12",
                exact_quote=(
                    "Data Lake là một kho lưu trữ "
                    "dữ liệu tập trung"
                ),
            ),
            clarification_question=None,
            next_action_hint=(
                "Xem Slide 12."
            ),
        )

        validate_response(
            response=response,
            request=self.request,
        )

    def test_fake_citation_is_blocked(self):

        response = ChatResponse(
            case="A",
            action="ANSWER_WITH_CITATION",
            reply_text=(
                "Data Lake giúp doanh nghiệp "
                "giảm 50% chi phí."
            ),
            citation=Citation(
                has_citation=True,
                source="Slide 12",
                exact_quote=(
                    "Data Lake giúp doanh nghiệp "
                    "giảm 50% chi phí."
                ),
            ),
            clarification_question=None,
            next_action_hint=(
                "Xem Slide 12."
            ),
        )

        with self.assertRaises(
            BackendValidationError
        ):
            validate_response(
                response=response,
                request=self.request,
            )


if __name__ == "__main__":
    unittest.main()