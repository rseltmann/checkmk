// Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
// This file is part of Checkmk (https://checkmk.com). It is subject to the
// terms and conditions defined in the file COPYING, which is part of this
// source code package.

#ifndef RendererJSON_h
#define RendererJSON_h

#include "config.h"  // IWYU pragma: keep

#include <iosfwd>
#include <string>
#include <vector>

#include "Renderer.h"
enum class Encoding;
class Logger;

class RendererJSON : public Renderer {
public:
    RendererJSON(std::ostream &os, Logger *logger, Encoding data_encoding);

    [[nodiscard]] bool useSurrogatePairs() const override;
    void outputNull() override;
    void outputBlob(const std::vector<char> &value) override;
    void outputString(const std::string &value) override;

    void beginQuery() override;
    void separateQueryElements() override;
    void endQuery() override;

    void beginRow() override;
    void beginRowElement() override;
    void endRowElement() override;
    void separateRowElements() override;
    void endRow() override;

    void beginList() override;
    void separateListElements() override;
    void endList() override;

    void beginSublist() override;
    void separateSublistElements() override;
    void endSublist() override;

    void beginDict() override;
    void separateDictElements() override;
    void separateDictKeyValue() override;
    void endDict() override;
};

#endif  // RendererJSON_h
