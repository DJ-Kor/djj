// SERVER 쪽에 설정
const { gql } = require("apollo-server");

const typeDef = gql`
  type LedosPoUpload {
    status: String
    region: String! # !는 필수
    country: String!
    project_name: String
    model_name: String!
    harmony: String
  }

  #Define Query Types
  extend type Query {
    getLedosPoUpload: [LedosPoUpload]
  }
  extend type Mutation {
    addLedOsPoUpload(lpu: LedosPoUpload): string # LedosPoUpload 가 input / string이 return
    updateLedOsPoUpload(lpu: LedosPoUpload): LEDOSBufferStock
    deleteLedosPoUpload(opportunity_code: String, model_names: [String]): Boolean # 반환 Boolean
  }
`;

const resolvers = {
  Query: {
    getLedosPoUpload: async (parent, {}, { models }) => {
      const ret = await models.LedosPoUpload.findAll();
      return ret;
    },
  },
  Mutation: {
    deleteLedosPoUpload: async (parent, { opportunity_code, model_names }, { models }) => {
      const ret = await models.LedosPoUpload.findAll({
        where: {
          opportunity_code: opportunity_code,
          model_name: {
            [Op.in]: model_names,
          },
        },
      });
      if (ret.length > 0) {
        await models.LedosPoUpload.destroy({
          where: {
            opportunity_code: opportunity_code,
            model_name: {
              [Op.in]: model_names,
            },
          },
        });
        return "deleted";
      }
      return "deleted";
    },
  },
};
