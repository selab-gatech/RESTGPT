import { APIResource } from 'openai/resource';
import { Completions } from './completions.js';
import * as API from './index.js';
export declare class Chat extends APIResource {
  completions: Completions;
}
export declare namespace Chat {
  export import Completions = API.Completions;
  export import ChatCompletion = API.ChatCompletion;
  export import ChatCompletionChunk = API.ChatCompletionChunk;
  export import ChatCompletionMessage = API.ChatCompletionMessage;
  export import CreateChatCompletionRequestMessage = API.CreateChatCompletionRequestMessage;
  export import CompletionCreateParams = API.CompletionCreateParams;
  export import CompletionCreateParamsNonStreaming = API.CompletionCreateParamsNonStreaming;
  export import CompletionCreateParamsStreaming = API.CompletionCreateParamsStreaming;
}
//# sourceMappingURL=chat.d.ts.map
