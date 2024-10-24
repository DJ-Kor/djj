// CLIENT 쪽에 설정

import { gql } from "@apollo/client"; // GraphQL query, mutation

// client side 변수
export const CLIENT_SIDE_VAR = gql`
  # 변수 opportunity (string) / model_names (string으로 이루어진 배열)
  mutation deleteLedosPos($opportunity_code: String, $model_names: [String]) {
    # 실제 요청 mutation
    deleteLedosPos(opportunity_code: $opportunity_code, model_names: $model_names)
  }
`;
